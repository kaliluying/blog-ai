"""
Blog AI 后端 API 主入口文件

本文件是 FastAPI 应用的入口点，定义了：
1. FastAPI 应用实例和全局配置
2. CORS 中间件配置
3. API 路由端点（CRUD 操作）
4. 数据模型转换函数

技术栈：
- FastAPI: Web 框架
- SQLAlchemy: ORM（异步支持）
- Pydantic: 数据验证
"""

# 标准库导入
import json
import secrets
from typing import List, Any

# 第三方库导入
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

# 环境配置
import os
import dotenv

# 加载 .env 环境变量
dotenv.load_dotenv()

# 内部模块导入
from database import get_db
from models import BlogPost, Comment
from schemas import (
    BlogPostCreate,
    BlogPostUpdate,
    BlogPostResponse,
    BlogPostListItem,
    CommentCreate,
    CommentResponse,
    SearchResult,
    ArchiveGroup,
    ArchiveYear,
    TitleCheckRequest,
    TitleCheckResponse,
)

from utils.time import utc_now


# ========== 管理员认证 Pydantic 模型 ==========

class AdminLoginRequest(BaseModel):
    """管理员登录请求"""
    password: str


class AdminLoginResponse(BaseModel):
    """管理员登录响应"""
    success: bool
    message: str
    token: str | None = None


# ========== 评论频率限制 ==========

from collections import defaultdict
from time import time

# 评论频率限制配置
COMMENT_RATE_LIMIT = 5  # 最多评论次数
COMMENT_RATE_WINDOW = 60  # 时间窗口（秒）

# 记录每个 IP 的评论时间戳
comment_rate_tracker: dict[str, list[float]] = defaultdict(list)


def check_comment_rate_limit(client_ip: str) -> bool:
    """
    检查评论频率限制

    Args:
        client_ip: 客户端 IP

    Returns:
        bool: True 表示可以评论，False 表示超出限制
    """
    now = time()
    # 清理过期的时间戳（保留窗口内的）
    comment_rate_tracker[client_ip] = [
        t for t in comment_rate_tracker[client_ip]
        if now - t < COMMENT_RATE_WINDOW
    ]
    # 检查是否超出限制
    if len(comment_rate_tracker[client_ip]) >= COMMENT_RATE_LIMIT:
        return False
    # 记录本次请求
    comment_rate_tracker[client_ip].append(now)
    return True


from crud import (
    get_posts,
    get_post_by_id,
    create_post,
    update_post,
    delete_post,
    search_posts,
    get_comments_by_post,
    get_comment_replies,
    create_comment,
    delete_comment,
    get_archive_posts_by_year_month,
    get_archive_years,
    get_archive_by_year,
    record_post_view,
    get_popular_posts,
    get_post_view_count,
    check_post_title_exists,
    get_related_posts,
)

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期事件处理器

    数据库迁移由 Alembic 管理（migrations/ 目录）
    """
    yield


# ========== 管理员认证依赖 ==========

# 从环境变量读取管理员密码
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# 旧版固定 token（用于兼容旧版本前端）
# TODO: 在前端升级后移除此兼容逻辑
ADMIN_TOKEN = "blog-admin-token"

# 有效的管理员 session tokens（内存存储，生产环境建议用 Redis）
valid_admin_tokens: set[str] = set()


def generate_admin_token() -> str:
    """生成管理员 session token"""
    return f"admin_{secrets.token_hex(32)}"


async def verify_admin_password(password: str) -> bool:
    """验证管理员密码"""
    return password == ADMIN_PASSWORD


async def get_current_admin(request: Request) -> bool:
    """
    验证管理员身份
    支持新版 session token 和旧版固定 token（向后兼容）

    Note:
        旧版固定 token 兼容将在后续版本移除
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要管理员权限",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.replace("Bearer ", "")

    # 验证 token（新版 session token 或旧版固定 token）
    if token not in valid_admin_tokens and token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的管理员令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return True


# ========== FastAPI 应用初始化 ==========

# 创建 FastAPI 应用实例
app = FastAPI(
    title="Blog AI API",
    description="手绘风格博客后端 API",
    version="1.0.0",
    lifespan=lifespan,
)

# ========== 中间件配置 ==========

# CORS（跨域资源共享）中间件配置
# 从环境变量读取允许的源，多个源用逗号分隔
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== 管理员认证路由 ==========


@app.post("/api/admin/login", response_model=AdminLoginResponse)
async def admin_login(request_body: AdminLoginRequest):
    """
    管理员登录

    验证密码后返回 session token。

    Request Body:
        password: 管理员密码（从环境变量 ADMIN_PASSWORD 读取）

    Returns:
        AdminLoginResponse: 登录结果及 token
    """
    password = request_body.password

    if not password:
        return AdminLoginResponse(
            success=False,
            message="请输入密码",
            token=None
        )

    if password == ADMIN_PASSWORD:
        # 生成新的 session token
        token = generate_admin_token()
        valid_admin_tokens.add(token)

        return AdminLoginResponse(
            success=True,
            message="登录成功",
            token=token
        )
    else:
        return AdminLoginResponse(
            success=False,
            message="密码错误",
            token=None
        )


@app.post("/api/admin/logout")
async def admin_logout(request: Request):
    """
    管理员登出

    使当前 session token 失效。
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        valid_admin_tokens.discard(token)

    return {"message": "已登出"}


# ========== 工具函数 ==========


# 月份名称映射
MONTH_NAMES = {
    1: "一月",
    2: "二月",
    3: "三月",
    4: "四月",
    5: "五月",
    6: "六月",
    7: "七月",
    8: "八月",
    9: "九月",
    10: "十月",
    11: "十一月",
    12: "十二月",
}


def parse_post_tags(post: BlogPost) -> List[str]:
    """解析文章的 tags 字段，处理 JSON 字符串和列表两种格式"""
    tags = post.tags if post.tags else []
    if isinstance(tags, str):
        try:
            tags = json.loads(tags)
        except (json.JSONDecodeError, TypeError):
            tags = []
    return tags if isinstance(tags, list) else []


def post_to_dict(post: BlogPost) -> dict:
    """将 BlogPost ORM 模型转换为完整字典"""
    now = utc_now()
    return {
        "id": post.id,
        "title": post.title,
        "excerpt": post.excerpt,
        "content": post.content,
        "date": post.date,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "tags": parse_post_tags(post),
        "view_count": post.view_count,
        "is_scheduled": post.date > now,  # 是否定时发布（未来时间）
    }


def post_to_list_item(post: BlogPost) -> dict:
    """将 BlogPost ORM 模型转换为列表项"""
    return {
        "id": post.id,
        "title": post.title,
        "excerpt": post.excerpt,
        "date": post.date,
        "tags": parse_post_tags(post),
        "view_count": post.view_count,
    }


def comment_to_dict(comment: Comment, nickname: str | None = None) -> dict:
    """将 Comment ORM 模型转换为字典（匿名评论使用 nickname）"""
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "nickname": nickname or "匿名用户",
        "content": comment.content,
        "parent_id": comment.parent_id,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
    }


def group_posts_by_month(posts: List[BlogPost], year: int) -> List[ArchiveGroup]:
    """将文章列表按月份分组"""
    months_data: dict[int, list[dict]] = {}

    for post in posts:
        post_date = post.date if hasattr(post.date, "month") else post.date.month
        month = (
            post_date.month
            if hasattr(post_date, "month")
            else int(post_date.split("-")[1])
        )

        if month not in months_data:
            months_data[month] = []
        months_data[month].append(post_to_list_item(post))

    months = []
    for month, posts_list in months_data.items():
        months.append(
            ArchiveGroup(
                year=year,
                month=month,
                month_name=MONTH_NAMES.get(month, str(month)),
                post_count=len(posts_list),
                posts=posts_list,
            )
        )

    # 按月份降序排序
    months.sort(key=lambda x: x.month, reverse=True)
    return months


# ========== API 路由 ==========


# ========== 文章搜索路由 ==========


@app.get("/api/search", response_model=List[SearchResult])
async def search_articles(
    q: str, skip: int = 0, limit: int = 50,
    include_scheduled: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    搜索文章

    Query Parameters:
        q: 搜索关键词
        skip: 分页偏移
        limit: 返回数量限制
        include_scheduled: 是否包含定时发布的文章

    Returns:
        List[SearchResult]: 搜索结果列表
    """
    posts = await search_posts(db, query=q, skip=skip, limit=limit, include_scheduled=include_scheduled)
    return [post_to_dict(p) for p in posts]


# ========== 评论路由 ==========

# 评论回复最大递归深度，防止无限递归
MAX_REPLY_DEPTH = 3


@app.get("/api/posts/{post_id}/comments")
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    """
    获取文章的评论列表

    Path Parameters:
        post_id: 文章 ID

    Returns:
        List[dict]: 评论列表（包含嵌套回复）
    """

    async def get_replies_recursive(parent_id: int, depth: int = 0) -> list:
        """递归获取所有层级的回复（带深度限制）"""
        if depth >= MAX_REPLY_DEPTH:
            return []
        replies = await get_comment_replies(db, parent_id)
        reply_list = []
        for reply in replies:
            reply_dict = comment_to_dict(reply, reply.nickname)
            # 递归获取子回复，传递深度参数
            reply_dict["replies"] = await get_replies_recursive(reply.id, depth + 1)
            reply_list.append(reply_dict)
        return reply_list

    # 获取顶级评论
    comments = await get_comments_by_post(db, post_id)

    result = []
    for comment in comments:
        # 获取回复（递归获取所有层级）
        reply_list = await get_replies_recursive(comment.id)

        comment_dict = comment_to_dict(comment, comment.nickname)
        comment_dict["replies"] = reply_list
        result.append(comment_dict)

    return result


@app.post(
    "/api/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED
)
async def create_comment_route(
    comment_data: CommentCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    创建匿名评论

    Request Body:
        post_id: 文章 ID
        nickname: 昵称
        content: 评论内容
        parent_id: 父评论 ID（可选，用于回复）

    Returns:
        CommentResponse: 创建的评论

    无需登录，任何人都可以发表评论
    """
    # 获取客户端 IP
    client_ip = request.headers.get("X-Real-IP", request.client.host)

    # 检查频率限制
    if not check_comment_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="评论过于频繁，请稍后再试"
        )

    # 验证文章是否存在
    post = await get_post_by_id(db, comment_data.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    # 验证父评论是否存在（如果提供了 parent_id）
    if comment_data.parent_id:
        parent_result = await db.execute(
            select(Comment.id).where(Comment.id == comment_data.parent_id)
        )
        if not parent_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="父评论不存在"
            )

    comment = await create_comment(
        db,
        post_id=comment_data.post_id,
        nickname=comment_data.nickname,
        content=comment_data.content,
        parent_id=comment_data.parent_id,
    )

    return comment_to_dict(comment, comment.nickname)


@app.delete("/api/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_route(
    comment_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    删除评论（仅管理员可操作）

    Path Parameters:
        comment_id: 评论 ID

    Returns:
        None: 204 状态码无响应体

    Requires Admin Authentication
    """
    await get_current_admin(request)

    # 获取评论
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="评论不存在")

    await db.delete(comment)
    await db.commit()


# ========== 文章路由 ==========


@app.get("/api/posts/count")
async def get_posts_count(db: AsyncSession = Depends(get_db)):
    """
    获取已发布文章总数

    Returns:
        dict: 文章总数
    """
    now = utc_now()

    result = await db.execute(
        select(func.count(BlogPost.id)).where(BlogPost.date <= now)
    )
    count = result.scalar_one_or_none() or 0

    return {"count": count}


@app.get("/api/posts")
async def list_posts(
    skip: int = 0, limit: int = 100,
    include_scheduled: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    获取文章列表

    Query Parameters:
        skip: 跳过的记录数（分页偏移），默认 0
        limit: 返回的最大记录数，默认 100
        include_scheduled: 是否包含定时发布的文章（仅管理员可用）

    Returns:
        List[dict]: 文章列表，每篇文章包含基本信息
    """
    posts = await get_posts(db, skip=skip, limit=limit, include_scheduled=include_scheduled)
    # 将 ORM 模型列表转换为字典列表
    return [post_to_dict(p) for p in posts]


@app.get("/api/posts/popular")
async def get_popular_posts_route(
    limit: int = 5,
    include_scheduled: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    获取热门文章排行

    Query Parameters:
        limit: 返回数量限制，默认 5
        include_scheduled: 是否包含定时发布的文章

    Returns:
        List[dict]: 热门文章列表
    """
    posts = await get_popular_posts(db, limit=limit, include_scheduled=include_scheduled)
    return [post_to_list_item(p) for p in posts]


@app.get("/api/posts/{post_id}")
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """
    获取单篇文章详情

    Path Parameters:
        post_id: 文章 ID

    Returns:
        dict: 文章详情

    Raises:
        HTTPException: 404 - 文章不存在
    """
    post = await get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")
    return post_to_dict(post)


@app.get("/api/posts/{post_id}/related")
async def get_related_posts_route(
    post_id: int,
    limit: int = 5,
    include_scheduled: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    获取相关文章推荐

    Path Parameters:
        post_id: 当前文章 ID

    Query Parameters:
        limit: 返回数量限制，默认 5
        include_scheduled: 是否包含定时发布的文章

    Returns:
        List[dict]: 相关文章列表
    """
    post = await get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    tags = parse_post_tags(post)
    if not tags:
        return []

    related = await get_related_posts(db, post_id, tags, limit, include_scheduled)
    return [post_to_list_item(p) for p in related]


@app.post("/api/posts/{post_id}/view")
async def record_post_view_route(
    post_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    记录文章浏览（同一 IP 24 小时内只计一次）

    Path Parameters:
        post_id: 文章 ID

    Returns:
        dict: 是否成功计数及当前阅读量
    """
    # 验证文章是否存在
    post = await get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    # 获取真实 IP（处理代理情况）
    client_ip = request.headers.get("X-Real-IP", request.client.host)

    # 记录浏览
    counted = await record_post_view(db, post_id, client_ip)

    # 返回当前阅读量
    current_count = await get_post_view_count(db, post_id)

    return {"counted": counted, "view_count": current_count}


@app.post("/api/posts/check-title")
async def check_post_title(
    request_body: TitleCheckRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    检查文章标题是否已存在

    用于创建或编辑文章时的实时验证。

    Request Body:
        TitleCheckRequest: 包含 title 和可选的 exclude_id

    Returns:
        TitleCheckResponse: 标题是否存在及提示信息

    Requires Admin Authentication
    """
    await get_current_admin(request)

    try:
        exists = await check_post_title_exists(db, request_body.title, request_body.exclude_id)

        if exists:
            return TitleCheckResponse(
                exists=True,
                message=f"标题「{request_body.title}」已存在，请使用其他标题"
            )
        else:
            return TitleCheckResponse(
                exists=False,
                message="标题可以使用"
            )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return TitleCheckResponse(
            exists=False,
            message=f"检查失败: {str(e)}"
        )


@app.post("/api/posts", status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post: BlogPostCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    创建新文章

    Request Body:
        BlogPostCreate: 包含 title, excerpt, content, tags

    Returns:
        dict: 创建的文章详情

    Status Code:
        201: 资源创建成功

    Requires Admin Authentication
    """
    await get_current_admin(request)

    created_post = await create_post(db, post, tags=post.tags)
    return post_to_dict(created_post)


@app.put("/api/posts/{post_id}")
async def update_existing_post(
    post_id: int,
    post_update: BlogPostUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    更新文章

    Path Parameters:
        post_id: 要更新的文章 ID

    Request Body:
        BlogPostUpdate: 要更新的字段（支持部分更新）

    Returns:
        dict: 更新后的文章详情

    Raises:
        HTTPException: 404 - 文章不存在

    Requires Admin Authentication
    """
    await get_current_admin(request)

    # 提取 tags（如果存在）
    tags = (
        post_update.tags
        if hasattr(post_update, "tags") and post_update.tags is not None
        else None
    )

    # 创建不包含 tags 的更新数据
    # BlogPostUpdate 包含 tags，但 BlogPost 模型不需要单独处理
    update_data = post_update.model_dump(exclude_unset=True)
    if "tags" in update_data:
        update_data.pop("tags")

    # 执行更新
    post = await update_post(db, post_id, BlogPostUpdate(**update_data), tags=tags)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")
    return post_to_dict(post)


@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_post(
    post_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    删除文章

    Path Parameters:
        post_id: 要删除的文章 ID

    Returns:
        None: 204 状态码无响应体

    Raises:
        HTTPException: 404 - 文章不存在

    Requires Admin Authentication
    """
    await get_current_admin(request)

    success = await delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")


# ========== 归档路由 ==========


@app.get("/api/archive", response_model=List[ArchiveYear])
async def get_archive_list(
    include_scheduled: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    获取文章归档列表

    按年份和月份分组返回所有已发布文章

    Query Parameters:
        include_scheduled: 是否包含定时发布的文章

    Returns:
        List[ArchiveYear]: 年度归档列表
    """
    years = await get_archive_years(db)
    result = []

    for year in years:
        posts = await get_archive_by_year(db, year, include_scheduled)
        months = group_posts_by_month(posts, year)
        result.append(ArchiveYear(year=year, post_count=len(posts), months=months))

    return result


@app.get("/api/archive/{year}", response_model=ArchiveYear)
async def get_archive_by_year_route(
    year: int,
    include_scheduled: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    获取指定年份的文章归档

    Path Parameters:
        year: 年份

    Query Parameters:
        include_scheduled: 是否包含定时发布的文章

    Returns:
        ArchiveYear: 年度归档信息
    """
    posts = await get_archive_by_year(db, year, include_scheduled)

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="该年份没有文章"
        )

    months = group_posts_by_month(posts, year)
    return ArchiveYear(year=year, post_count=len(posts), months=months)


@app.get("/api/archive/{year}/{month}", response_model=ArchiveGroup)
async def get_archive_by_year_month_route(
    year: int,
    month: int,
    include_scheduled: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    获取指定年月的文章归档

    Path Parameters:
        year: 年份
        month: 月份 (1-12)

    Query Parameters:
        include_scheduled: 是否包含定时发布的文章

    Returns:
        ArchiveGroup: 月度归档信息
    """
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="月份必须在 1-12 之间"
        )

    posts = await get_archive_posts_by_year_month(db, year, month, include_scheduled)

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{year}年{month}月没有文章"
        )

    return ArchiveGroup(
        year=year,
        month=month,
        month_name=MONTH_NAMES.get(month, str(month)),
        post_count=len(posts),
        posts=[post_to_list_item(p) for p in posts],
    )


# ========== 应用启动入口 ==========

if __name__ == "__main__":
    import uvicorn

    # 使用 uvicorn ASGI 服务器运行应用
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)

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
from typing import List, Any

# 第三方库导入
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# 环境配置
import os
import dotenv

# 加载 .env 环境变量
dotenv.load_dotenv()

# 内部模块导入
from database import get_db, init_db
from models import BlogPost, User, Comment
from schemas import (
    BlogPostCreate,
    BlogPostUpdate,
    BlogPostResponse,
    BlogPostListItem,
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    CommentCreate,
    CommentResponse,
    CommentWithReplies,
    SearchResult,
    ArchiveGroup,
    ArchiveYear,
)
from crud import (
    get_posts,
    get_post_by_id,
    create_post,
    update_post,
    delete_post,
    get_user_by_username,
    get_user_by_email,
    create_user,
    get_user_by_id,
    search_posts,
    get_comments_by_post,
    get_comment_replies,
    create_comment,
    delete_comment,
    get_archive_posts_by_year_month,
    get_archive_years,
    get_archive_by_year,
)
from auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
    oauth2_scheme,
)

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期事件处理器

    在应用启动时初始化数据库表结构
    """
    await init_db()
    yield
    # 这里可以添加应用关闭时的清理逻辑


# ========== 认证依赖函数 ==========


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> dict:
    """
    获取当前登录用户

    作为 FastAPI 依赖使用，保护需要认证的路由。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="请先登录",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    # 确保 user_id 是整数
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 查询用户
    from sqlalchemy import select

    result = await db.execute(
        select(User).where(User.id == user_id, User.is_active == True)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "created_at": user.created_at,
    }


async def get_current_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    获取当前用户并验证是否为管理员
    """
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="需要管理员权限"
        )
    return current_user


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
# 允许前端开发服务器访问 API
app.add_middleware(
    CORSMiddleware,
    # 允许的来源列表（前端开发服务器地址）
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,  # 允许携带凭证（cookies）
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)


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


def post_to_dict(post: BlogPost) -> dict:
    """将 BlogPost ORM 模型转换为完整字典"""
    return {
        "id": post.id,
        "title": post.title,
        "excerpt": post.excerpt,
        "content": post.content,
        "date": post.date,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "tags": json.loads(post.tags) if post.tags else [],
    }


def post_to_list_item(post: BlogPost) -> dict:
    """将 BlogPost ORM 模型转换为列表项"""
    return {
        "id": post.id,
        "title": post.title,
        "excerpt": post.excerpt,
        "date": post.date,
        "tags": json.loads(post.tags) if post.tags else [],
    }


def user_to_dict(user: User) -> dict:
    """将 User ORM 模型转换为字典"""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "created_at": user.created_at,
    }


def comment_to_dict(comment: Comment, username: str = None) -> dict:
    """将 Comment ORM 模型转换为字典"""
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "user_id": comment.user_id,
        "username": username or "Unknown",
        "content": comment.content,
        "parent_id": comment.parent_id,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
    }


# ========== API 路由 ==========


# ========== 认证路由 ==========


@app.post("/api/auth/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    用户注册

    Request Body:
        username: 用户名
        email: 邮箱
        password: 密码

    Returns:
        Token: 访问令牌和用户信息
    """
    # 检查用户名是否已存在
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已被注册"
        )

    # 检查邮箱是否已存在
    existing_email = await get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已被注册"
        )

    # 密码长度检查
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="密码长度至少为6位"
        )

    # 创建用户
    hashed_password = get_password_hash(user_data.password)
    # 第一个注册的用户为管理员
    user_count = await db.execute(text("SELECT COUNT(*) FROM users"))
    is_admin = user_count.scalar() == 0

    db_user = await create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_admin=is_admin,
    )

    # 生成令牌
    access_token = create_access_token(data={"sub": db_user.id})

    return {"access_token": access_token, "user": user_to_dict(db_user)}


@app.post("/api/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    用户登录

    Request Body (form-data):
        username: 用户名
        password: 密码

    Returns:
        Token: 访问令牌和用户信息
    """
    # 查找用户
    user = await get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    # 验证密码
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    # 检查账户状态
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="账户已被禁用"
        )

    # 生成令牌
    access_token = create_access_token(data={"sub": user.id})

    return {"access_token": access_token, "user": user_to_dict(user)}


@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    获取当前登录用户信息

    Returns:
        UserResponse: 当前用户信息
    """
    return current_user


# ========== 文章搜索路由 ==========


@app.get("/api/search", response_model=List[SearchResult])
async def search_articles(
    q: str, skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)
):
    """
    搜索文章

    Query Parameters:
        q: 搜索关键词
        skip: 分页偏移
        limit: 返回数量限制

    Returns:
        List[SearchResult]: 搜索结果列表
    """
    posts = await search_posts(db, query=q, skip=skip, limit=limit)
    return [post_to_dict(p) for p in posts]


# ========== 评论路由 ==========


@app.get("/api/posts/{post_id}/comments")
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    """
    获取文章的评论列表

    Path Parameters:
        post_id: 文章 ID

    Returns:
        List[dict]: 评论列表（包含嵌套回复）
    """

    async def get_replies_recursive(parent_id: int) -> list:
        """递归获取所有层级的回复"""
        replies = await get_comment_replies(db, parent_id)
        reply_list = []
        for reply in replies:
            reply_user = await get_user_by_id(db, reply.user_id)
            reply_username = reply_user.username if reply_user else "Unknown"
            reply_dict = comment_to_dict(reply, reply_username)
            # 递归获取子回复
            reply_dict["replies"] = await get_replies_recursive(reply.id)
            reply_list.append(reply_dict)
        return reply_list

    # 获取顶级评论
    comments = await get_comments_by_post(db, post_id)

    result = []
    for comment in comments:
        # 获取评论者用户名
        user = await get_user_by_id(db, comment.user_id)
        username = user.username if user else "Unknown"

        # 获取回复（递归获取所有层级）
        reply_list = await get_replies_recursive(comment.id)

        comment_dict = comment_to_dict(comment, username)
        comment_dict["replies"] = reply_list
        result.append(comment_dict)

    return result


@app.post(
    "/api/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED
)
async def create_comment_route(
    comment_data: CommentCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    创建评论

    Request Body:
        post_id: 文章 ID
        content: 评论内容
        parent_id: 父评论 ID（可选，用于回复）

    Returns:
        CommentResponse: 创建的评论

    Requires Authentication
    """
    # 验证文章是否存在
    post = await get_post_by_id(db, comment_data.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    # 验证父评论是否存在（如果提供了 parent_id）
    if comment_data.parent_id:
        from sqlalchemy import select

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
        user_id=current_user["id"],
        content=comment_data.content,
        parent_id=comment_data.parent_id,
    )

    return comment_to_dict(comment, current_user["username"])


@app.delete("/api/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_route(
    comment_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    删除评论

    Path Parameters:
        comment_id: 评论 ID

    Returns:
        None: 204 状态码无响应体

    Requires Authentication
    只有评论作者或管理员可以删除评论
    """
    # 获取评论
    from sqlalchemy import select

    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="评论不存在")

    # 检查权限：只有评论作者或管理员可以删除
    if comment.user_id != current_user["id"] and not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="无权删除此评论"
        )

    await db.delete(comment)
    await db.commit()


# ========== 文章路由 ==========


@app.get("/api/posts")
async def list_posts(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    获取文章列表

    Query Parameters:
        skip: 跳过的记录数（分页偏移），默认 0
        limit: 返回的最大记录数，默认 100

    Returns:
        List[dict]: 文章列表，每篇文章包含基本信息
    """
    posts = await get_posts(db, skip=skip, limit=limit)
    # 将 ORM 模型列表转换为字典列表
    return [post_to_dict(p) for p in posts]


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


@app.post("/api/posts", status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post: BlogPostCreate,
    current_user: dict = Depends(get_current_admin),
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
    created_post = await create_post(db, post, tags=post.tags)
    return post_to_dict(created_post)


@app.put("/api/posts/{post_id}")
async def update_existing_post(
    post_id: int,
    post_update: BlogPostUpdate,
    current_user: dict = Depends(get_current_admin),
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
    current_user: dict = Depends(get_current_admin),
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
    success = await delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")


# ========== 归档路由 ==========


@app.get("/api/archive", response_model=List[ArchiveYear])
async def get_archive_list(db: AsyncSession = Depends(get_db)):
    """
    获取文章归档列表

    按年份和月份分组返回所有文章

    Returns:
        List[ArchiveYear]: 年度归档列表
    """
    years = await get_archive_years(db)
    result = []

    for year in years:
        posts = await get_archive_by_year(db, year)
        months_data = {}

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
        result.append(ArchiveYear(year=year, post_count=len(posts), months=months))

    return result


@app.get("/api/archive/{year}", response_model=ArchiveYear)
async def get_archive_by_year_route(
    year: int,
    db: AsyncSession = Depends(get_db),
):
    """
    获取指定年份的文章归档

    Path Parameters:
        year: 年份

    Returns:
        ArchiveYear: 年度归档信息
    """
    posts = await get_archive_by_year(db, year)

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="该年份没有文章"
        )

    months_data = {}

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

    months.sort(key=lambda x: x.month, reverse=True)

    return ArchiveYear(year=year, post_count=len(posts), months=months)


@app.get("/api/archive/{year}/{month}", response_model=ArchiveGroup)
async def get_archive_by_year_month_route(
    year: int,
    month: int,
    db: AsyncSession = Depends(get_db),
):
    """
    获取指定年月的文章归档

    Path Parameters:
        year: 年份
        month: 月份 (1-12)

    Returns:
        ArchiveGroup: 月度归档信息
    """
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="月份必须在 1-12 之间"
        )

    posts = await get_archive_posts_by_year_month(db, year, month)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)

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
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

# 环境配置
import os
import dotenv

# 加载 .env 环境变量
dotenv.load_dotenv()

# 内部模块导入
from database import get_db, init_db
from models import BlogPost
from schemas import BlogPostCreate, BlogPostUpdate, BlogPostResponse, BlogPostListItem
from crud import get_posts, get_post_by_id, create_post, update_post, delete_post

# ========== FastAPI 应用初始化 ==========

# 创建 FastAPI 应用实例
app = FastAPI(
    title="Blog AI API",
    description="手绘风格博客后端 API",
    version="1.0.0"
)

# ========== 中间件配置 ==========

# CORS（跨域资源共享）中间件配置
# 允许前端开发服务器访问 API
app.add_middleware(
    CORSMiddleware,
    # 允许的来源列表（前端开发服务器地址）
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,           # 允许携带凭证（cookies）
    allow_methods=["*"],              # 允许所有 HTTP 方法
    allow_headers=["*"],              # 允许所有请求头
)


# ========== 工具函数 ==========

def post_to_dict(post: BlogPost) -> dict:
    """
    将 BlogPost ORM 模型转换为字典

    处理说明：
    - ORM 模型中的 tags 字段是 JSON 字符串存储
    - 需要转换为 Python 列表返回给前端

    Args:
        post: BlogPost ORM 模型实例

    Returns:
        dict: 包含文章数据的字典，tags 为列表类型
    """
    return {
        "id": post.id,
        "title": post.title,
        "excerpt": post.excerpt,
        "content": post.content,
        "date": post.date,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        # 将 JSON 字符串解析为列表，若为空则返回空列表
        "tags": json.loads(post.tags) if post.tags else []
    }


# ========== 生命周期事件 ==========

@app.on_event("startup")
async def startup():
    """
    应用启动事件处理器

    在应用启动时初始化数据库表结构
    """
    await init_db()


# ========== API 路由 ==========

@app.get("/", response_model=dict)
async def root():
    """
    根路径 - API 健康检查

    Returns:
        dict: 欢迎消息和 API 文档链接
    """
    return {"message": "欢迎使用 Blog AI API", "docs": "/docs"}


@app.get("/api/posts")
async def list_posts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    return post_to_dict(post)


@app.post("/api/posts", status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post: BlogPostCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新文章

    Request Body:
        BlogPostCreate: 包含 title, excerpt, content, tags

    Returns:
        dict: 创建的文章详情

    Status Code:
        201: 资源创建成功
    """
    created_post = await create_post(db, post, tags=post.tags)
    return post_to_dict(created_post)


@app.put("/api/posts/{post_id}")
async def update_existing_post(
    post_id: int,
    post_update: BlogPostUpdate,
    db: AsyncSession = Depends(get_db)
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
    """
    # 提取 tags（如果存在）
    tags = post_update.tags if hasattr(post_update, 'tags') and post_update.tags is not None else None

    # 创建不包含 tags 的更新数据
    # BlogPostUpdate 包含 tags，但 BlogPost 模型不需要单独处理
    update_data = post_update.model_dump(exclude_unset=True)
    if 'tags' in update_data:
        update_data.pop('tags')

    # 执行更新
    post = await update_post(db, post_id, BlogPostUpdate(**update_data), tags=tags)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    return post_to_dict(post)


@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    删除文章

    Path Parameters:
        post_id: 要删除的文章 ID

    Returns:
        None: 204 状态码无响应体

    Raises:
        HTTPException: 404 - 文章不存在
    """
    success = await delete_post(db, post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )


# ========== 应用启动入口 ==========

if __name__ == "__main__":
    import uvicorn

    # 使用 uvicorn ASGI 服务器运行应用
    uvicorn.run(app, host="0.0.0.0", port=8000)

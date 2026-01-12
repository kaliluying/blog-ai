import json
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
import os
import dotenv

dotenv.load_dotenv()

from database import get_db, init_db
from models import BlogPost
from schemas import BlogPostCreate, BlogPostUpdate, BlogPostResponse, BlogPostListItem
from crud import get_posts, get_post_by_id, create_post, update_post, delete_post

app = FastAPI(
    title="Blog AI API",
    description="手绘风格博客后端 API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def post_to_dict(post: BlogPost) -> dict:
    """将 BlogPost 模型转换为字典，处理 tags 字段"""
    return {
        "id": post.id,
        "title": post.title,
        "excerpt": post.excerpt,
        "content": post.content,
        "date": post.date,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "tags": json.loads(post.tags) if post.tags else []
    }


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/", response_model=dict)
async def root():
    return {"message": "欢迎使用 Blog AI API", "docs": "/docs"}


@app.get("/api/posts")
async def list_posts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """获取所有文章列表"""
    posts = await get_posts(db, skip=skip, limit=limit)
    return [post_to_dict(p) for p in posts]


@app.get("/api/posts/{post_id}")
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """获取单篇文章详情"""
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
    """创建新文章"""
    created_post = await create_post(db, post, tags=post.tags)
    return post_to_dict(created_post)


@app.put("/api/posts/{post_id}")
async def update_existing_post(
    post_id: int,
    post_update: BlogPostUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新文章"""
    # 提取 tags 如果存在
    tags = post_update.tags if hasattr(post_update, 'tags') and post_update.tags is not None else None

    # 创建不包含 tags 的更新数据（因为 BlogPostUpdate 有 tags 但 BlogPost 模型不需要它）
    update_data = post_update.model_dump(exclude_unset=True)
    if 'tags' in update_data:
        update_data.pop('tags')

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
    """删除文章"""
    success = await delete_post(db, post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

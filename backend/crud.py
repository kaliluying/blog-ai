import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import BlogPost
from schemas import BlogPostCreate, BlogPostUpdate
from datetime import datetime, timezone
from typing import List, Optional


def utc_now():
    """返回当前 UTC 时间（naive datetime for PostgreSQL compatibility）"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def tags_to_json(tags: List[str]) -> str:
    return json.dumps(tags, ensure_ascii=False)


def tags_from_json(json_str: str) -> List[str]:
    try:
        return json.loads(json_str) if json_str else []
    except (json.JSONDecodeError, TypeError):
        return []


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[BlogPost]:
    result = await db.execute(
        select(BlogPost)
        .order_by(BlogPost.date.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_post_by_id(db: AsyncSession, post_id: int) -> Optional[BlogPost]:
    result = await db.execute(
        select(BlogPost).where(BlogPost.id == post_id)
    )
    return result.scalar_one_or_none()


async def create_post(db: AsyncSession, post: BlogPostCreate, tags: List[str] = None) -> BlogPost:
    tags_json = tags_to_json(tags or [])
    db_post = BlogPost(
        title=post.title,
        excerpt=post.excerpt,
        content=post.content,
        tags=tags_json,
        date=utc_now()
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def update_post(db: AsyncSession, post_id: int, post_update: BlogPostUpdate, tags: List[str] = None) -> Optional[BlogPost]:
    db_post = await get_post_by_id(db, post_id)
    if not db_post:
        return None

    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)

    # Handle tags separately if provided
    if tags is not None:
        db_post.tags = tags_to_json(tags)

    await db.commit()
    await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, post_id: int) -> bool:
    db_post = await get_post_by_id(db, post_id)
    if not db_post:
        return False

    await db.delete(db_post)
    await db.commit()
    return True

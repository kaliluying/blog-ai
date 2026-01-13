"""
数据库 CRUD 操作模块

本模块封装所有数据库操作函数：
- get_posts: 获取文章列表
- get_post_by_id: 获取单篇文章
- create_post: 创建文章
- update_post: 更新文章
- delete_post: 删除文章

技术要点：
- 使用 SQLAlchemy 异步 API
- 支持分页查询（skip/limit）
- 辅助函数处理 JSON 和时间戳

辅助函数：
- utc_now: 获取当前 UTC 时间
- tags_to_json: 将标签列表转为 JSON 字符串
- tags_from_json: 将 JSON 字符串转为标签列表
"""

# 标准库导入
import json
from datetime import datetime, timezone
from typing import List, Optional

# 第三方库导入
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, text

# 内部模块导入
from models import BlogPost, User, Comment
from schemas import BlogPostCreate, BlogPostUpdate


# ========== 辅助函数 ==========


def utc_now():
    """
    获取当前 UTC 时间

    返回不带时区信息的 datetime 对象（naive datetime），
    以确保与 PostgreSQL 的 timestamp 类型兼容。

    Returns:
        datetime: 当前 UTC 时间（无时区）
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


def tags_to_json(tags: List[str]) -> str:
    """
    将标签列表转换为 JSON 字符串

    Args:
        tags: 标签字符串列表

    Returns:
        str: JSON 格式的字符串
    """
    return json.dumps(tags, ensure_ascii=False)


def tags_from_json(json_str: str) -> List[str]:
    """
    将 JSON 字符串转换为标签列表

    Args:
        json_str: JSON 格式的字符串

    Returns:
        List[str]: 标签字符串列表
    """
    try:
        return json.loads(json_str) if json_str else []
    except (json.JSONDecodeError, TypeError):
        # 解析失败时返回空列表
        return []


# ========== 用户相关 CRUD ==========


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """根据用户名获取用户"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """根据邮箱获取用户"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """根据 ID 获取用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    hashed_password: str,
    is_admin: bool = False,
) -> User:
    """创建新用户"""
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_admin=is_admin,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# ========== 文章相关 CRUD ==========


async def get_posts(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[BlogPost]:
    """
    获取文章列表

    支持分页查询，按日期降序排序（最新的在前）。

    Args:
        db: 数据库会话
        skip: 跳过的记录数（分页偏移），默认 0
        limit: 返回的最大记录数，默认 100

    Returns:
        List[BlogPost]: 文章 ORM 模型列表
    """
    # 构建查询：按日期降序排列，分页
    result = await db.execute(
        select(BlogPost)
        .order_by(BlogPost.date.desc())  # 降序：最新的在前
        .offset(skip)  # 分页偏移
        .limit(limit)  # 返回数量限制
    )
    # 获取所有结果
    return result.scalars().all()


async def get_post_by_id(db: AsyncSession, post_id: int) -> Optional[BlogPost]:
    """
    根据 ID 获取单篇文章

    Args:
        db: 数据库会话
        post_id: 文章 ID

    Returns:
        Optional[BlogPost]: 找到的文章 ORM 模型，未找到返回 None
    """
    result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
    # scalar_one_or_none: 返回唯一结果或 None
    return result.scalar_one_or_none()


async def create_post(
    db: AsyncSession, post: BlogPostCreate, tags: List[str] = None
) -> BlogPost:
    """
    创建新文章

    Args:
        db: 数据库会话
        post: 创建文章的数据（来自请求体）
        tags: 标签列表，若为 None 则使用 post.tags

    Returns:
        BlogPost: 创建的文章 ORM 模型
    """
    # 处理标签列表
    tags_json = tags_to_json(tags or [])

    # 创建 ORM 模型实例
    db_post = BlogPost(
        title=post.title,
        excerpt=post.excerpt,
        content=post.content,
        tags=tags_json,
        date=utc_now(),
    )

    # 添加到会话并提交
    db.add(db_post)
    await db.commit()

    # 刷新以获取数据库生成的值（如 ID）
    await db.refresh(db_post)

    return db_post


async def update_post(
    db: AsyncSession, post_id: int, post_update: BlogPostUpdate, tags: List[str] = None
) -> Optional[BlogPost]:
    """
    更新文章

    支持部分更新，只更新提供的字段。
    如果 tags 参数提供，则同时更新标签。

    Args:
        db: 数据库会话
        post_id: 要更新的文章 ID
        post_update: 更新数据（部分更新）
        tags: 可选的新标签列表

    Returns:
        Optional[BlogPost]: 更新后的文章，未找到返回 None
    """
    # 先获取原文章
    db_post = await get_post_by_id(db, post_id)
    if not db_post:
        return None

    # 获取更新数据的字典
    update_data = post_update.model_dump(exclude_unset=True)

    # 更新每个字段
    for field, value in update_data.items():
        setattr(db_post, field, value)

    # 单独处理 tags 字段（如果提供）
    if tags is not None:
        db_post.tags = tags_to_json(tags)

    # 提交事务
    await db.commit()

    # 刷新以获取更新后的数据
    await db.refresh(db_post)

    return db_post


async def delete_post(db: AsyncSession, post_id: int) -> bool:
    """
    删除文章

    Args:
        db: 数据库会话
        post_id: 要删除的文章 ID

    Returns:
        bool: 删除成功返回 True，文章不存在返回 False
    """
    # 获取要删除的文章
    db_post = await get_post_by_id(db, post_id)
    if not db_post:
        return False

    # 从会话中删除并提交
    await db.delete(db_post)
    await db.commit()

    return True


async def search_posts(
    db: AsyncSession, query: str, skip: int = 0, limit: int = 100
) -> List[BlogPost]:
    """
    搜索文章

    在标题和内容中搜索关键词。

    Args:
        db: 数据库会话
        query: 搜索关键词
        skip: 分页偏移
        limit: 返回数量限制

    Returns:
        List[BlogPost]: 匹配的文章列表
    """
    # 使用 ILIKE 进行大小写不敏感搜索
    search_pattern = f"%{query}%"
    result = await db.execute(
        select(BlogPost)
        .where(
            or_(
                BlogPost.title.ilike(search_pattern),
                BlogPost.content.ilike(search_pattern),
                BlogPost.excerpt.ilike(search_pattern),
            )
        )
        .order_by(BlogPost.date.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


# ========== 评论相关 CRUD ==========


async def get_comments_by_post(db: AsyncSession, post_id: int) -> List[Comment]:
    """获取文章的所有顶级评论"""
    result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id, Comment.parent_id.is_(None))
        .order_by(Comment.created_at.desc())
    )
    return result.scalars().all()


async def get_comment_replies(db: AsyncSession, parent_id: int) -> List[Comment]:
    """获取评论的所有回复"""
    result = await db.execute(
        select(Comment)
        .where(Comment.parent_id == parent_id)
        .order_by(Comment.created_at.asc())
    )
    return result.scalars().all()


async def create_comment(
    db: AsyncSession,
    post_id: int,
    user_id: int,
    content: str,
    parent_id: Optional[int] = None,
) -> Comment:
    """创建评论"""
    db_comment = Comment(
        post_id=post_id, user_id=user_id, content=content, parent_id=parent_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def delete_comment(db: AsyncSession, comment_id: int) -> bool:
    """删除评论"""
    db_comment = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = db_comment.scalar_one_or_none()
    if not comment:
        return False

    await db.delete(comment)
    await db.commit()
    return True


# ========== 归档相关 CRUD ==========


async def get_archive_posts_by_year_month(
    db: AsyncSession, year: int, month: int
) -> List[BlogPost]:
    """
    获取指定年月的文章列表

    Args:
        db: 数据库会话
        year: 年份
        month: 月份 (1-12)

    Returns:
        List[BlogPost]: 该年月的文章列表
    """
    # 计算该月的起始和结束时间
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    result = await db.execute(
        select(BlogPost)
        .where(BlogPost.date >= start_date, BlogPost.date < end_date)
        .order_by(BlogPost.date.desc())
    )
    return result.scalars().all()


async def get_archive_years(db: AsyncSession) -> List[int]:
    """
    获取所有有文章的年份列表

    Args:
        db: 数据库会话

    Returns:
        List[int]: 有文章的年份列表（降序）
    """
    # 使用原生 SQL 提取年份（表名是 blog_posts）
    result = await db.execute(
        text(
            "SELECT DISTINCT EXTRACT(YEAR FROM date)::int as year FROM blog_posts ORDER BY year DESC"
        )
    )
    years = [row[0] for row in result.fetchall() if row[0]]
    return years


async def get_archive_by_year(db: AsyncSession, year: int) -> List[BlogPost]:
    """
    获取指定年份的所有文章

    Args:
        db: 数据库会话
        year: 年份

    Returns:
        List[BlogPost]: 该年份的文章列表
    """
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    result = await db.execute(
        select(BlogPost)
        .where(BlogPost.date >= start_date, BlogPost.date < end_date)
        .order_by(BlogPost.date.desc())
    )
    return result.scalars().all()

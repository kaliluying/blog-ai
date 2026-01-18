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
- tags 字段使用 JSON 类型，无需手动序列化
"""

# 标准库导入
from datetime import datetime, timedelta
from typing import List, Optional

# 第三方库导入
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, text, func, distinct

# 内部模块导入
from models import BlogPost, Comment
from schemas import BlogPostCreate, BlogPostUpdate
from utils.time import utc_now


# ========== 文章相关 CRUD ==========


async def get_posts(
    db: AsyncSession, skip: int = 0, limit: int = 100, include_scheduled: bool = False
) -> List[BlogPost]:
    """
    获取文章列表

    支持分页查询，按日期降序排序（最新的在前）。
    默认只返回已发布的文章（date <= now）。

    Args:
        db: 数据库会话
        skip: 跳过的记录数（分页偏移），默认 0
        limit: 返回的最大记录数，默认 100
        include_scheduled: 是否包含定时发布的文章（管理员使用）

    Returns:
        List[BlogPost]: 文章 ORM 模型列表
    """
    now = utc_now()

    # 构建查询：按日期降序排列，分页
    query = select(BlogPost)

    # 非管理员模式下，过滤未发布的文章
    if not include_scheduled:
        query = query.where(BlogPost.date <= now)

    result = await db.execute(
        query
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


async def check_post_title_exists(
    db: AsyncSession,
    title: str,
    exclude_id: Optional[int] = None
) -> bool:
    """
    检查文章标题是否已存在

    用于创建或更新文章时验证标题唯一性。

    Args:
        db: 数据库会话
        title: 要检查的标题
        exclude_id: 排除的文章 ID（更新时使用）

    Returns:
        bool: 标题已存在返回 True，不存在返回 False
    """
    query = select(BlogPost).where(BlogPost.title == title)
    if exclude_id is not None:
        query = query.where(BlogPost.id != exclude_id)
    query = query.limit(1)  # 限制只返回一条记录
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


async def create_post(
    db: AsyncSession, post: BlogPostCreate, tags: List[str] | None = None
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
    # 确定发布日期：如果指定了 publish_date 则使用，否则使用当前时间
    publish_date = post.publish_date if post.publish_date else utc_now()

    # 创建 ORM 模型实例
    db_post = BlogPost(
        title=post.title,
        excerpt=post.excerpt,
        content=post.content,
        tags=tags or [],
        date=publish_date,
    )

    # 添加到会话并提交
    db.add(db_post)
    await db.commit()

    # 刷新以获取数据库生成的值（如 ID）
    await db.refresh(db_post)

    return db_post


async def update_post(
    db: AsyncSession, post_id: int, post_update: BlogPostUpdate, tags: List[str] | None = None
) -> Optional[BlogPost]:
    """
    更新文章

    支持部分更新，只更新提供的字段。
    如果 tags 参数提供，则同时更新标签。
    如果提供了 publish_date，则更新文章的 date 字段。

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
        db_post.tags = tags

    # 单独处理 publish_date（如果提供）
    if post_update.publish_date is not None:
        db_post.date = post_update.publish_date

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
    db: AsyncSession, query: str, skip: int = 0, limit: int = 100, include_scheduled: bool = False
) -> List[BlogPost]:
    """
    搜索文章

    在标题和内容中搜索关键词。
    默认只返回已发布的文章。

    Args:
        db: 数据库会话
        query: 搜索关键词
        skip: 分页偏移
        limit: 返回数量限制
        include_scheduled: 是否包含定时发布的文章

    Returns:
        List[BlogPost]: 匹配的文章列表
    """
    now = utc_now()

    # 使用 ILIKE 进行大小写不敏感搜索
    search_pattern = f"%{query}%"
    sql = select(BlogPost).where(
        or_(
            BlogPost.title.ilike(search_pattern),
            BlogPost.content.ilike(search_pattern),
            BlogPost.excerpt.ilike(search_pattern),
        )
    )

    # 非管理员模式下，过滤未发布的文章
    if not include_scheduled:
        sql = sql.where(BlogPost.date <= now)

    result = await db.execute(
        sql.order_by(BlogPost.date.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


# ========== 评论相关 CRUD ==========


async def get_comments_by_post(db: AsyncSession, post_id: int, sort: str = "newest") -> List[Comment]:
    """获取文章的所有顶级评论

    Args:
        db: 数据库会话
        post_id: 文章 ID
        sort: 排序方式，'newest' 最新优先（默认），'oldest' 最早优先
    """
    # 根据排序方式选择排序方向
    order_func = Comment.created_at.desc() if sort == "newest" else Comment.created_at.asc()

    result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id, Comment.parent_id.is_(None))
        .order_by(order_func)
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
    nickname: str,
    content: str,
    parent_id: Optional[int] = None,
) -> Comment:
    """创建匿名评论"""
    db_comment = Comment(
        post_id=post_id, nickname=nickname, content=content, parent_id=parent_id
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
    db: AsyncSession, year: int, month: int, include_scheduled: bool = False
) -> List[BlogPost]:
    """
    获取指定年月的文章列表

    Args:
        db: 数据库会话
        year: 年份
        month: 月份 (1-12)
        include_scheduled: 是否包含定时发布的文章

    Returns:
        List[BlogPost]: 该年月的文章列表
    """
    now = utc_now()

    # 计算该月的起始和结束时间
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    sql = select(BlogPost).where(
        BlogPost.date >= start_date,
        BlogPost.date < end_date
    )

    # 非管理员模式下，过滤未发布的文章
    if not include_scheduled:
        sql = sql.where(BlogPost.date <= now)

    result = await db.execute(
        sql.order_by(BlogPost.date.desc())
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
    # 使用 SQLAlchemy 的 func.extract 提取年份（替代原生 SQL）
    result = await db.execute(
        select(distinct(func.extract('YEAR', BlogPost.date).label('year')))
        .order_by(func.extract('YEAR', BlogPost.date).desc())
    )
    years = [int(row[0]) for row in result.fetchall() if row[0]]
    return years


async def get_archive_by_year(
    db: AsyncSession, year: int, include_scheduled: bool = False
) -> List[BlogPost]:
    """
    获取指定年份的所有文章

    Args:
        db: 数据库会话
        year: 年份
        include_scheduled: 是否包含定时发布的文章

    Returns:
        List[BlogPost]: 该年份的文章列表
    """
    now = utc_now()

    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    sql = select(BlogPost).where(
        BlogPost.date >= start_date,
        BlogPost.date < end_date
    )

    # 非管理员模式下，过滤未发布的文章
    if not include_scheduled:
        sql = sql.where(BlogPost.date <= now)

    result = await db.execute(
        sql.order_by(BlogPost.date.desc())
    )
    return result.scalars().all()


async def get_post_view_count(db: AsyncSession, post_id: int) -> int:
    """
    获取文章阅读量

    Args:
        db: 数据库会话
        post_id: 文章 ID

    Returns:
        int: 阅读量
    """
    # 直接查询 view_count 字段，避免获取整个文章对象
    result = await db.execute(
        select(BlogPost.view_count).where(BlogPost.id == post_id)
    )
    return result.scalar_one_or_none() or 0


async def increment_post_view(db: AsyncSession, post_id: int) -> bool:
    """
    增加文章阅读量（原子操作）

    Args:
        db: 数据库会话
        post_id: 文章 ID

    Returns:
        bool: 是否成功增加
    """
    from sqlalchemy import update

    result = await db.execute(
        update(BlogPost)
        .where(BlogPost.id == post_id)
        .values(view_count=BlogPost.view_count + 1)
    )
    await db.commit()
    return result.rowcount > 0


async def check_view_record_exists(db: AsyncSession, post_id: int, ip: str) -> bool:
    """
    检查该 IP 是否在 24 小时内已记录过浏览

    Args:
        db: 数据库会话
        post_id: 文章 ID
        ip: 客户端 IP

    Returns:
        bool: 是否已存在记录
    """
    # 查找 24 小时内该 IP 是否已有记录
    result = await db.execute(
        text("""
            SELECT 1 FROM post_view_ips
            WHERE post_id = :post_id AND ip = :ip
            AND viewed_at > :expired_at
            LIMIT 1
        """),
        {
            "post_id": post_id,
            "ip": ip,
            "expired_at": utc_now() - timedelta(hours=24)
        }
    )
    return result.scalar_one_or_none() is not None


async def record_post_view(db: AsyncSession, post_id: int, ip: str) -> bool:
    """
    记录文章浏览（同一 IP 24 小时内只计一次）

    Args:
        db: 数据库会话
        post_id: 文章 ID
        ip: 客户端 IP

    Returns:
        bool: 是否成功计数（False 表示已在 24 小时内记录过）
    """
    now = utc_now()

    # 检查是否已记录
    if await check_view_record_exists(db, post_id, ip):
        return False

    # 记录新浏览（使用 ON CONFLICT DO NOTHING 处理并发）
    result = await db.execute(
        text("""
            INSERT INTO post_view_ips (post_id, ip, viewed_at)
            VALUES (:post_id, :ip, :viewed_at)
            ON CONFLICT (post_id, ip) DO NOTHING
        """),
        {
            "post_id": post_id,
            "ip": ip,
            "viewed_at": now
        }
    )

    # 只有插入新记录时才增加阅读量
    if result.rowcount > 0:
        await increment_post_view(db, post_id)

    return True


async def get_popular_posts(
    db: AsyncSession, limit: int = 5, include_scheduled: bool = False
) -> List[BlogPost]:
    """
    获取热门文章排行

    Args:
        db: 数据库会话
        limit: 返回数量限制
        include_scheduled: 是否包含定时发布的文章

    Returns:
        List[BlogPost]: 按阅读量降序排列的文章列表
    """
    now = utc_now()

    sql = select(BlogPost).order_by(BlogPost.view_count.desc())

    # 非管理员模式下，过滤未发布的文章
    if not include_scheduled:
        sql = sql.where(BlogPost.date <= now)

    result = await db.execute(sql.limit(limit))
    return result.scalars().all()


async def get_related_posts(
    db: AsyncSession,
    post_id: int,
    tags: List[str],
    limit: int = 5,
    include_scheduled: bool = False
) -> List[BlogPost]:
    """
    获取相关文章推荐

    基于标签匹配查找相关文章，按匹配数和阅读量排序。

    Args:
        db: 数据库会话
        post_id: 当前文章 ID（排除）
        tags: 当前文章的标签列表
        limit: 返回数量限制
        include_scheduled: 是否包含定时发布的文章

    Returns:
        List[BlogPost]: 相关文章列表
    """
    if not tags:
        return []

    now = utc_now()

    # 构建标签匹配条件 - 使用 jsonb_exists 并确保类型转换兼容
    tag_conditions = []
    params = {"post_id": post_id, "limit": limit, "now": now}
    for i, tag in enumerate(tags[:5]):
        tag_conditions.append(f"jsonb_exists(p.tags::jsonb, :tag{i})")
        params[f"tag{i}"] = tag

    # 构建 WHERE 子句
    where_clause = f"p.id != :post_id AND ({' OR '.join(tag_conditions)})"
    if not include_scheduled:
        where_clause += " AND p.date <= :now"

    # 使用子查询避免 GROUP BY 问题
    result = await db.execute(
        text(f"""
            SELECT p.*
            FROM blog_posts p
            WHERE {where_clause}
            ORDER BY p.view_count DESC
            LIMIT :limit
        """),
        params
    )

    rows = result.fetchall()
    return [row[0] for row in rows] if rows else []


async def cleanup_expired_view_records(db: AsyncSession, days: int = 30) -> int:
    """
    清理过期的浏览记录

    Args:
        db: 数据库会话
        days: 保留天数，默认 30 天

    Returns:
        int: 删除的记录数
    """
    result = await db.execute(
        text("""
            DELETE FROM post_view_ips
            WHERE viewed_at < :expired_at
        """),
        {
            "expired_at": utc_now() - timedelta(days=days)
        }
    )
    await db.commit()
    return result.rowcount

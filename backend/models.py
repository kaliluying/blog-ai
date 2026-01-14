"""
SQLAlchemy ORM 数据模型定义模块

本模块定义博客系统的数据库表结构：
- BlogPost: 博客文章模型
- User: 用户模型
- Comment: 评论模型

技术要点：
- 使用 SQLAlchemy 2.0 的 Mapped 类型注解风格
- 支持索引、默认值、约束条件
- 时间戳自动管理（创建/更新时间）
- 使用 JSON 类型存储标签

注意事项：
- 使用 timezone-aware datetime（UTC）存储时间
- tags 字段使用 PostgreSQL JSON 类型
"""

# 标准库导入
from datetime import datetime
from typing import List

# 第三方库导入
from sqlalchemy import String, Text, DateTime, Boolean, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

# 内部模块导入
from database import Base
from utils.time import utc_now


class User(Base):
    """
    用户模型

    对应数据库表：users

    字段说明：
    - id: 主键，自增
    - username: 用户名，唯一索引
    - email: 邮箱，唯一索引
    - hashed_password: 加密后的密码
    - is_active: 是否激活
    - is_admin: 是否管理员
    - created_at: 创建时间
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Comment(Base):
    """
    评论模型

    对应数据库表：comments

    字段说明：
    - id: 主键，自增
    - post_id: 关联的文章 ID
    - user_id: 评论者 ID
    - content: 评论内容
    - parent_id: 父评论 ID（用于回复）
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id})>"


class BlogPost(Base):
    """
    博客文章模型

    对应数据库表：blog_posts

    字段说明：
    - id: 主键，自增
    - title: 文章标题，索引加速搜索
    - excerpt: 文章摘要/简介
    - content: 文章完整内容（支持 Markdown）
    - tags: 标签列表（JSON 类型）
    - date: 发布日期
    - created_at: 创建时间（自动设置）
    - updated_at: 更新时间（更新时自动刷新）
    - view_count: 阅读量
    """
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[List[str]] = mapped_column(JSON, default=list)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    def __repr__(self):
        """
        对象字符串表示

        Returns:
            str: 格式化的对象描述
        """
        return f"<BlogPost(id={self.id}, title='{self.title}')>"

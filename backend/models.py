"""
SQLAlchemy ORM 数据模型定义模块

本模块定义博客系统的数据库表结构：
- BlogPost: 博客文章模型
- Comment: 评论模型

技术要点：
- 使用 SQLAlchemy 2.0 的 Mapped 类型注解风格
- 支持索引、默认值、约束条件
- 时间戳自动管理（创建/更新时间）
- 使用 JSON 类型存储标签

注意事项：
- 使用 timezone-aware datetime（UTC）存储时间
- tags 字段使用 PostgreSQL JSON 类型
- 用户系统已简化为仅博主管理，无需用户注册登录
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


class Comment(Base):
    """
    评论模型（匿名评论）

    对应数据库表：comments

    字段说明：
    - id: 主键，自增
    - post_id: 关联的文章 ID
    - nickname: 评论者昵称（匿名）
    - content: 评论内容
    - parent_id: 父评论 ID（用于回复）
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(nullable=False, index=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id}, nickname='{self.nickname}')>"


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

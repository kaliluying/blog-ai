"""
SQLAlchemy ORM 数据模型定义模块

本模块定义博客系统的数据库表结构：
- BlogPost: 博客文章模型
- User: 用户模型
- Comment: 评论模型

技术要点：
- 使用 SQLAlchemy Column 类型定义字段
- 支持索引、默认值、约束条件
- 时间戳自动管理（创建/更新时间）

注意事项：
- tags 字段以 JSON 字符串形式存储在 Text 字段中
- 使用 naive datetime（无时区信息）以兼容 PostgreSQL
"""

# 标准库导入
from datetime import datetime

# 第三方库导入
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

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

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)

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

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

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
    - tags: 标签列表（JSON 字符串存储）
    - date: 发布日期
    - created_at: 创建时间（自动设置）
    - updated_at: 更新时间（更新时自动刷新）
    """
    # 表名
    __tablename__ = "blog_posts"

    # 主键
    id = Column(Integer, primary_key=True, index=True)

    # 标题：最大长度 255 字符，非空，索引
    title = Column(String(255), nullable=False, index=True)

    # 摘要：文本类型，非空
    excerpt = Column(Text, nullable=False)

    # 内容：完整文章内容，非空
    content = Column(Text, nullable=False)

    # 标签：JSON 数组存储为文本，默认空数组
    tags = Column(Text, default='[]')

    # 发布日期：默认为当前时间
    date = Column(DateTime, default=utc_now)

    # 创建时间：默认为当前时间
    created_at = Column(DateTime, default=utc_now)

    # 更新时间：默认为当前时间，更新时自动刷新
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    def __repr__(self):
        """
        对象字符串表示

        Returns:
            str: 格式化的对象描述
        """
        return f"<BlogPost(id={self.id}, title='{self.title}')>"

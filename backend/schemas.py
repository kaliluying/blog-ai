"""
Pydantic 数据验证模式（Schemas）模块

本模块定义 API 请求和响应的数据结构：
- 请求模式：创建和更新文章时的数据验证
- 响应模式：API 返回给前端的数据结构

技术要点：
- 继承 Pydantic 的 BaseModel
- 支持数据验证、类型检查
- 支持可选字段和默认值

类说明：
- BlogPostBase: 基础模式，包含所有文章共有字段
- BlogPostCreate: 创建文章时的请求模式
- BlogPostUpdate: 更新文章时的请求模式
- BlogPostResponse: 文章详情响应模式
- BlogPostListItem: 列表页简化响应模式
"""

# 标准库导入
from datetime import datetime

# 第三方库导入
from pydantic import BaseModel, EmailStr
from typing import List, Optional


# ========== 用户相关模式 ==========


class UserBase(BaseModel):
    """用户基础模式"""

    username: str
    email: EmailStr


class UserCreate(UserBase):
    """创建用户请求模式"""

    password: str


class UserLogin(BaseModel):
    """用户登录请求模式"""

    username: str
    password: str


class UserResponse(UserBase):
    """用户响应模式"""

    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token 响应模式"""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token 数据模式"""

    username: Optional[str] = None
    user_id: Optional[int] = None


# ========== 文章相关模式 ==========


class BlogPostBase(BaseModel):
    """
    博客文章基础模式

    包含文章的核心字段，作为其他模式的基类。
    """

    title: str  # 文章标题
    excerpt: str  # 文章摘要
    content: str  # 文章内容


class BlogPostCreate(BlogPostBase):
    """
    创建文章请求模式

    继承基础字段，添加创建时特有的字段。
    """

    tags: List[str] = []  # 标签列表，默认空列表


class BlogPostUpdate(BlogPostBase):
    """
    更新文章请求模式

    所有字段都是可选的，支持部分更新。
    """

    title: Optional[str] = None  # 可选更新
    excerpt: Optional[str] = None  # 可选更新
    content: Optional[str] = None  # 可选更新
    tags: Optional[List[str]] = None  # 可选更新


class BlogPostResponse(BlogPostBase):
    """
    文章详情响应模式

    用于 API 返回完整文章信息。
    """

    id: int  # 文章 ID
    date: datetime  # 发布日期
    created_at: datetime  # 创建时间
    updated_at: datetime  # 更新时间
    tags: List[str] = []  # 标签列表
    view_count: int = 0  # 阅读量

    class Config:
        """
        Pydantic 配置

        from_attributes: 允许从 ORM 模型创建 Pydantic 模型
        """

        from_attributes = True


# 用于列表返回的简化响应模式
class BlogPostListItem(BaseModel):
    """
    文章列表项响应模式

    用于文章列表页的简化展示。
    """

    id: int  # 文章 ID
    title: str  # 标题
    excerpt: str  # 摘要
    date: datetime  # 发布日期
    tags: List[str] = []  # 标签
    view_count: int = 0  # 阅读量

    class Config:
        """
        Pydantic 配置

        from_attributes: 允许从 ORM 模型创建 Pydantic 模型
        """

        from_attributes = True


# ========== 评论相关模式 ==========


class CommentBase(BaseModel):
    """评论基础模式"""

    content: str


class CommentCreate(CommentBase):
    """创建评论请求模式"""

    post_id: int
    parent_id: Optional[int] = None  # 回复的评论 ID


class CommentResponse(CommentBase):
    """评论响应模式"""

    id: int
    post_id: int
    user_id: int
    username: str  # 评论者用户名
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommentWithReplies(CommentResponse):
    """带回复的评论响应模式"""

    replies: List[CommentResponse] = []


# ========== 搜索相关模式 ==========


class SearchResult(BaseModel):
    """搜索结果模式"""

    id: int
    title: str
    excerpt: str
    date: datetime
    tags: List[str] = []
    score: Optional[float] = None  # 搜索相关性得分

    class Config:
        from_attributes = True


# ========== 归档相关模式 ==========


class ArchiveGroup(BaseModel):
    """归档分组模式

    按年月分组的文章归档
    """

    year: int  # 年份
    month: int  # 月份 (1-12)
    month_name: str  # 月份名称 (如 "一月")
    post_count: int  # 该月的文章数量
    posts: List[BlogPostListItem] = []  # 该月的文章列表

    class Config:
        from_attributes = True


class ArchiveYear(BaseModel):
    """年度归档模式

    按年份分组的归档
    """

    year: int  # 年份
    post_count: int  # 该年的文章数量
    months: List[ArchiveGroup] = []  # 该年的月份归档列表

    class Config:
        from_attributes = True

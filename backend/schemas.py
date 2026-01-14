"""
Pydantic 数据验证模式（Schemas）模块

本模块定义 API 请求和响应的数据结构：
- 请求模式：创建和更新文章时的数据验证
- 响应模式：API 返回给前端的数据结构

技术要点：
- 使用 Pydantic v2 的 BaseModel
- 支持数据验证、类型检查
- 支持可选字段和默认值
- 使用 model_config 替代 Config 类

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
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import List, Optional
import re


# ========== 用户相关模式 ==========


class UserBase(BaseModel):
    """用户基础模式"""

    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr


class UserCreate(UserBase):
    """创建用户请求模式"""

    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """验证密码复杂度"""
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('密码必须包含至少一个字母')
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含至少一个数字')
        return v


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

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj) -> "UserResponse":
        """从 ORM 对象创建 Pydantic 模型"""
        return cls.model_validate(obj)


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
    """博客文章基础模式"""

    title: str = Field(..., min_length=1, max_length=255)
    excerpt: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)


class BlogPostCreate(BlogPostBase):
    """创建文章请求模式"""

    tags: List[str] = []


class BlogPostUpdate(BlogPostBase):
    """更新文章请求模式"""

    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class TitleCheckRequest(BaseModel):
    """标题唯一性检查请求模式"""

    title: str = Field(..., min_length=1, max_length=255)
    exclude_id: Optional[int] = None


class TitleCheckResponse(BaseModel):
    """标题唯一性检查响应模式"""

    exists: bool
    message: str


class BlogPostResponse(BlogPostBase):
    """文章详情响应模式"""

    id: int
    date: datetime
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []
    view_count: int = 0

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj) -> "BlogPostResponse":
        """从 ORM 对象创建 Pydantic 模型"""
        return cls.model_validate(obj)


class BlogPostListItem(BaseModel):
    """文章列表项响应模式"""

    id: int
    title: str
    excerpt: str
    date: datetime
    tags: List[str] = []
    view_count: int = 0

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj) -> "BlogPostListItem":
        """从 ORM 对象创建 Pydantic 模型"""
        return cls.model_validate(obj)


# ========== 评论相关模式 ==========


class CommentBase(BaseModel):
    """评论基础模式"""

    content: str = Field(..., min_length=1, max_length=2000)


class CommentCreate(CommentBase):
    """创建评论请求模式"""

    post_id: int
    parent_id: Optional[int] = None


class CommentResponse(CommentBase):
    """评论响应模式"""

    id: int
    post_id: int
    user_id: int
    username: str
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj) -> "CommentResponse":
        """从 ORM 对象创建 Pydantic 模型"""
        return cls.model_validate(obj)


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
    score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj) -> "SearchResult":
        """从 ORM 对象创建 Pydantic 模型"""
        return cls.model_validate(obj)


# ========== 归档相关模式 ==========


class ArchiveGroup(BaseModel):
    """归档分组模式"""

    year: int
    month: int
    month_name: str
    post_count: int
    posts: List[BlogPostListItem] = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj) -> "ArchiveGroup":
        """从 ORM 对象创建 Pydantic 模型"""
        return cls.model_validate(obj)


class ArchiveYear(BaseModel):
    """年度归档模式"""

    year: int
    post_count: int
    months: List[ArchiveGroup] = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj) -> "ArchiveYear":
        """从 ORM 对象创建 Pydantic 模型"""
        return cls.model_validate(obj)

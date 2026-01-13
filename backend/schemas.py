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
from pydantic import BaseModel
from typing import List, Optional


class BlogPostBase(BaseModel):
    """
    博客文章基础模式

    包含文章的核心字段，作为其他模式的基类。
    """
    title: str          # 文章标题
    excerpt: str        # 文章摘要
    content: str        # 文章内容


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
    title: Optional[str] = None       # 可选更新
    excerpt: Optional[str] = None     # 可选更新
    content: Optional[str] = None     # 可选更新
    tags: Optional[List[str]] = None  # 可选更新


class BlogPostResponse(BlogPostBase):
    """
    文章详情响应模式

    用于 API 返回完整文章信息。
    """
    id: int                 # 文章 ID
    date: datetime          # 发布日期
    created_at: datetime    # 创建时间
    updated_at: datetime    # 更新时间
    tags: List[str] = []    # 标签列表

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
    id: int              # 文章 ID
    title: str           # 标题
    excerpt: str         # 摘要
    date: datetime       # 发布日期
    tags: List[str] = [] # 标签

    class Config:
        """
        Pydantic 配置

        from_attributes: 允许从 ORM 模型创建 Pydantic 模型
        """
        from_attributes = True

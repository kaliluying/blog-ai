from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class BlogPostBase(BaseModel):
    title: str
    excerpt: str
    content: str


class BlogPostCreate(BlogPostBase):
    tags: List[str] = []


class BlogPostUpdate(BlogPostBase):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class BlogPostResponse(BlogPostBase):
    id: int
    date: datetime
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []

    class Config:
        from_attributes = True


# 用于列表返回的简化响应
class BlogPostListItem(BaseModel):
    id: int
    title: str
    excerpt: str
    date: datetime
    tags: List[str] = []

    class Config:
        from_attributes = True

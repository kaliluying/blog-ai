from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base


def utc_now():
    """返回当前 UTC 时间（naive datetime for PostgreSQL compatibility）"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    excerpt = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(Text, default='[]')  # JSON array stored as text
    date = Column(DateTime, default=utc_now)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    def __repr__(self):
        return f"<BlogPost(id={self.id}, title='{self.title}')>"

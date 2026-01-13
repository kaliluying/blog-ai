"""
数据库连接和初始化模块

本模块负责：
1. 创建 SQLAlchemy 异步数据库引擎
2. 配置数据库会话工厂
3. 定义依赖注入函数获取数据库会话
4. 提供数据库初始化函数

技术栈：
- SQLAlchemy Core + AsyncIO
- asyncpg: PostgreSQL 异步驱动
"""

# 标准库导入
import os

# 第三方库导入
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 加载环境变量
load_dotenv()

# ========== 数据库配置 ==========

# 数据库连接 URL
# 优先级：环境变量 DATABASE_URL > 默认值
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/blog_ai"
)

# 创建异步数据库引擎
# echo=True: 启用 SQL 日志（开发环境使用）
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建异步会话工厂
# expire_on_commit=False: 提交后不立即过期对象，提高性能
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# declarative_base: 用于创建 ORM 模型基类
Base = declarative_base()


# ========== 依赖注入 ==========


async def get_db():
    """
    异步数据库会话依赖注入函数

    使用 FastAPI 的 Depends 机制提供数据库会话：
    1. 创建一个新的异步会话
    2. 尝试执行业务逻辑
    3. 无论成功或失败，确保会话正确关闭

    Yields:
        AsyncSession: 数据库会话实例

    示例：
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            # 使用 db 执行查询
            pass
    """
    async with async_session() as session:
        try:
            # 成功时自动提交
            yield session
        finally:
            # 无论成功失败，都关闭会话
            await session.close()


# ========== 数据库初始化 ==========


async def init_db():
    """
    初始化数据库表结构

    在应用启动时调用，创建所有定义的数据库表。
    使用 SQLAlchemy 的 run_sync 方法同步执行 DDL。
    """
    # 导入模型，确保 metadata 包含所有表定义
    from models import BlogPost, User, Comment

    async with engine.begin() as conn:
        # 创建所有继承自 Base 的模型对应的表
        await conn.run_sync(Base.metadata.create_all)

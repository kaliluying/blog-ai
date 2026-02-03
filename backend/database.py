"""
数据库连接和初始化模块

本模块负责：
1. 创建 SQLAlchemy 异步数据库引擎
2. 配置数据库会话工厂
3. 定义依赖注入函数获取数据库会话
4. 提供数据库初始化函数

技术栈：
- SQLAlchemy 2.0 Core + AsyncIO
- asyncpg: PostgreSQL 异步驱动
"""

# 标准库导入
import os
from typing import List

# 第三方库导入
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.dialects import mysql

# 加载环境变量
load_dotenv()

# ========== 数据库配置 ==========

# 数据库连接 URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is required. "
        "Example: mysql+aiomysql://user:password@localhost:3306/blog"
    )

# 创建异步数据库引擎
# echo: 从环境变量读取，默认关闭 SQL 日志（生产环境）
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"
engine = create_async_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
)

# 创建异步会话工厂
# expire_on_commit=False: 提交后不立即过期对象，提高性能
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# DeclarativeBase: SQLAlchemy 2.0 推荐的 ORM 模型基类
# 配置类型映射：Python list[str] 映射到 MySQL JSON 类型
class Base(DeclarativeBase):
    type_annotation_map = {
        List[str]: mysql.JSON,
    }


# ========== 依赖注入 ==========


async def get_db():
    """
    异步数据库会话依赖注入函数

    使用 FastAPI 的 Depends 机制提供数据库会话：
    1. 创建一个新的异步会话
    2. 尝试执行业务逻辑
    3. 异常时自动回滚，确保事务一致性
    4. 无论成功或失败，确保会话正确关闭

    注意：
    - CRUD 函数中需要显式调用 await db.commit() 来提交事务
    - 异常会自动触发 rollback

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
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ========== 数据库初始化 ==========


async def init_db():
    """
    初始化数据库表结构

    在应用启动时调用，创建所有定义的数据库表。
    使用 SQLAlchemy 2.0 的 run_sync 方法同步执行 DDL。
    """
    raise RuntimeError("init_db 已禁用，请使用 Alembic 迁移管理数据库表")

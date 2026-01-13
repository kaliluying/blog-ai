"""
测试配置文件

包含测试夹具（fixtures）和全局配置
"""

import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


# 使用内存 SQLite 数据库进行测试
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 创建测试引擎
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 创建会话工厂
TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环实例"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_database():
    """在每个测试前创建表，测试后删除表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncSession:
    """提供测试数据库会话"""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncClient:
    """提供测试客户端"""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

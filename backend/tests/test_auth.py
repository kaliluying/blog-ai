"""
管理员认证 API 测试

测试管理员登录与受保护接口访问
"""

import pytest


async def get_admin_token(client) -> str:
    response = await client.post("/api/admin/login", json={"password": "admin123"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["token"]
    return data["token"]


@pytest.mark.asyncio
async def test_admin_login_success(client):
    """测试管理员登录成功"""
    token = await get_admin_token(client)
    assert token


@pytest.mark.asyncio
async def test_admin_login_wrong_password(client):
    """测试管理员密码错误"""
    response = await client.post("/api/admin/login", json={"password": "wrongpassword"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["token"] is None


@pytest.mark.asyncio
async def test_admin_stats_unauthorized(client):
    """测试未授权访问管理接口"""
    response = await client.get("/api/admin/stats")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_admin_stats_authorized(client):
    """测试授权访问管理接口"""
    token = await get_admin_token(client)
    response = await client.get(
        "/api/admin/stats", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

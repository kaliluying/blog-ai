"""
认证 API 测试

测试用户注册、登录和认证相关功能
"""

import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    """测试用户注册功能"""
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "testuser"
    assert data["user"]["is_admin"] is True  # 第一个用户是管理员


@pytest.mark.asyncio
async def test_register_duplicate_username(client):
    """测试重复用户名注册"""
    # 第一次注册
    await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test1@example.com",
            "password": "testpassword123",
        },
    )

    # 重复注册
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 400
    assert "用户名已被注册" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client):
    """测试登录成功"""
    # 先注册
    await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )

    # 登录
    response = await client.post(
        "/api/auth/login", data={"username": "testuser", "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """测试密码错误登录"""
    # 注册用户
    await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )

    # 错误密码登录
    response = await client.post(
        "/api/auth/login", data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "用户名或密码错误" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_me_unauthorized(client):
    """测试未授权访问当前用户"""
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authorized(client):
    """测试授权访问当前用户"""
    # 注册并登录
    await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )

    login_response = await client.post(
        "/api/auth/login", data={"username": "testuser", "password": "testpassword123"}
    )
    token = login_response.json()["access_token"]

    # 获取当前用户
    response = await client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

"""
文章 API 测试

测试文章 CRUD 操作
"""

import pytest
import json


@pytest.mark.asyncio
async def test_create_post(client):
    """测试创建文章（需要管理员权限）"""
    # 先注册管理员用户
    await client.post(
        "/api/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
        },
    )

    # 登录获取 token
    login_response = await client.post(
        "/api/auth/login", data={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]

    # 创建文章
    response = await client.post(
        "/api/posts",
        json={
            "title": "测试文章",
            "excerpt": "这是测试摘要",
            "content": "这是测试内容，支持 Markdown",
            "tags": ["测试", "前端"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试文章"
    assert data["tags"] == ["测试", "前端"]
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_create_post_without_auth(client):
    """测试未授权创建文章"""
    response = await client.post(
        "/api/posts",
        json={
            "title": "测试文章",
            "excerpt": "这是测试摘要",
            "content": "这是测试内容",
            "tags": ["测试"],
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_posts(client):
    """测试获取文章列表"""
    # 先创建一篇文章
    await client.post(
        "/api/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
        },
    )

    login_response = await client.post(
        "/api/auth/login", data={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]

    await client.post(
        "/api/posts",
        json={
            "title": "测试文章",
            "excerpt": "摘要",
            "content": "内容",
            "tags": ["测试"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # 获取文章列表
    response = await client.get("/api/posts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_single_post(client):
    """测试获取单篇文章"""
    # 创建文章
    await client.post(
        "/api/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
        },
    )

    login_response = await client.post(
        "/api/auth/login", data={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]

    create_response = await client.post(
        "/api/posts",
        json={
            "title": "测试文章",
            "excerpt": "摘要",
            "content": "内容",
            "tags": ["测试"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    post_id = create_response.json()["id"]

    # 获取单篇文章
    response = await client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "测试文章"


@pytest.mark.asyncio
async def test_get_nonexistent_post(client):
    """测试获取不存在的文章"""
    response = await client.get("/api/posts/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_post(client):
    """测试更新文章"""
    # 创建文章
    await client.post(
        "/api/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
        },
    )

    login_response = await client.post(
        "/api/auth/login", data={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]

    create_response = await client.post(
        "/api/posts",
        json={
            "title": "原始标题",
            "excerpt": "原始摘要",
            "content": "原始内容",
            "tags": ["测试"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    post_id = create_response.json()["id"]

    # 更新文章
    response = await client.put(
        f"/api/posts/{post_id}",
        json={
            "title": "更新后的标题",
            "excerpt": "更新后的摘要",
            "content": "更新后的内容",
            "tags": ["测试", "更新"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "更新后的标题"


@pytest.mark.asyncio
async def test_delete_post(client):
    """测试删除文章"""
    # 创建文章
    await client.post(
        "/api/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
        },
    )

    login_response = await client.post(
        "/api/auth/login", data={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]

    create_response = await client.post(
        "/api/posts",
        json={
            "title": "待删除的文章",
            "excerpt": "摘要",
            "content": "内容",
            "tags": ["测试"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    post_id = create_response.json()["id"]

    # 删除文章
    response = await client.delete(
        f"/api/posts/{post_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    # 验证已删除
    get_response = await client.get(f"/api/posts/{post_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_search_posts(client):
    """测试搜索文章"""
    # 创建文章
    await client.post(
        "/api/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
        },
    )

    login_response = await client.post(
        "/api/auth/login", data={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]

    await client.post(
        "/api/posts",
        json={
            "title": "Python 教程",
            "excerpt": "学习 Python",
            "content": "Python 是一门优秀的语言",
            "tags": ["Python"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # 搜索
    response = await client.get("/api/search?q=Python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "Python" in data[0]["title"]

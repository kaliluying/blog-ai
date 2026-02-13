# Blog AI API 文档

基于 `backend/main.py` 与 `backend/schemas.py` 整理。

## 基础信息

- Base URL（开发）：`http://localhost:8000`
- 所有接口前缀：`/api`
- 认证方式：管理员接口使用 `Authorization: Bearer <token>`
- 内容类型：`application/json`

## 认证与权限

- `POST /api/admin/login` 登录成功后返回 JWT
- 需要管理员权限的接口：
  - `/api/posts/check-title`
  - `POST /api/posts`
  - `PUT /api/posts/{post_id}`
  - `DELETE /api/posts/{post_id}`
  - `DELETE /api/comments/{comment_id}`
  - `/api/admin/stats`
  - `/api/admin/comments`
  - `/api/admin/settings`（GET/POST）
- 部分公开接口带 `include_scheduled=true` 时也需要管理员权限：
  - `/api/search`
  - `/api/posts`
  - `/api/posts/popular`
  - `/api/posts/{post_id}/related`
  - `/api/archive`
  - `/api/archive/{year}`
  - `/api/archive/{year}/{month}`

## 数据模型（核心）

### BlogPostCreate

```json
{
  "title": "string",
  "excerpt": "string",
  "content": "string",
  "tags": ["tag1", "tag2"],
  "publish_date": "2026-02-13T12:00:00Z"
}
```

### BlogPostUpdate

```json
{
  "title": "string",
  "excerpt": "string",
  "content": "string",
  "tags": ["tag1", "tag2"],
  "publish_date": "2026-02-13T12:00:00Z"
}
```

### CommentCreate

```json
{
  "post_id": 1,
  "nickname": "访客",
  "content": "评论内容",
  "parent_id": 10
}
```

## 接口清单

### 1) 管理员认证

#### POST `/api/admin/login`

- 请求体：

```json
{
  "password": "string"
}
```

- 响应：

```json
{
  "success": true,
  "message": "登录成功",
  "token": "jwt-token"
}
```

#### POST `/api/admin/logout`

- 说明：无状态登出，主要由前端清理 token
- 响应：

```json
{
  "message": "已登出"
}
```

---

### 2) 文章相关

#### GET `/api/posts`

- Query：
  - `skip` (int, default 0)
  - `limit` (int, default 100)
  - `include_scheduled` (bool, default false；为 true 时需管理员)
- 响应：文章列表

#### GET `/api/posts/count`

- 响应：

```json
{ "count": 12 }
```

#### GET `/api/posts/{post_id}`

- 响应：单篇文章详情
- 错误：`404 文章不存在`

#### GET `/api/posts/popular`

- Query：
  - `limit` (int, default 5)
  - `include_scheduled` (bool, default false；为 true 时需管理员)
- 响应：热门文章列表（列表项结构）

#### GET `/api/posts/{post_id}/related`

- Query：
  - `limit` (int, default 5)
  - `include_scheduled` (bool, default false；为 true 时需管理员)
- 响应：相关文章列表
- 错误：`404 文章不存在`，`500 获取相关文章失败`

#### POST `/api/posts/{post_id}/view`

- 说明：同一 IP 24 小时内只计一次
- 响应：

```json
{
  "counted": true,
  "view_count": 123
}
```

#### POST `/api/posts/check-title`（管理员）

- 请求体：

```json
{
  "title": "文章标题",
  "excludeId": 1
}
```

- 响应：

```json
{
  "exists": false,
  "message": "标题可以使用"
}
```

#### POST `/api/posts`（管理员）

- 请求体：`BlogPostCreate`
- 响应：创建后的文章详情
- 状态码：`201 Created`

#### PUT `/api/posts/{post_id}`（管理员）

- 请求体：`BlogPostUpdate`
- 响应：更新后的文章详情
- 错误：`404 文章不存在`

#### DELETE `/api/posts/{post_id}`（管理员）

- 响应：无内容
- 状态码：`204 No Content`
- 错误：`404 文章不存在`

---

### 3) 搜索

#### GET `/api/search`

- Query：
  - `q` (string, 必填)
  - `skip` (int, default 0)
  - `limit` (int, default 50)
  - `include_scheduled` (bool, default false；为 true 时需管理员)
- 响应：`SearchResult[]`

---

### 4) 评论

#### GET `/api/posts/{post_id}/comments`

- Query：
  - `sort`: `newest | oldest`（默认 `newest`）
- 响应：评论树（包含 `replies`）

#### POST `/api/comments`

- 请求体：`CommentCreate`
- 响应：`CommentResponse`
- 状态码：`201 Created`
- 错误：
  - `404 文章不存在`
  - `404 父评论不存在`
  - `429 评论过于频繁，请稍后再试`

#### DELETE `/api/comments/{comment_id}`（管理员）

- 响应：无内容
- 状态码：`204 No Content`
- 错误：`404 评论不存在`

---

### 5) 归档

#### GET `/api/archive`

- Query：`include_scheduled` (bool, default false；true 时需管理员)
- 响应：`ArchiveYear[]`

#### GET `/api/archive/{year}`

- Query：`include_scheduled` (bool, default false；true 时需管理员)
- 响应：`ArchiveYear`
- 错误：`404 该年份没有文章`

#### GET `/api/archive/{year}/{month}`

- Query：`include_scheduled` (bool, default false；true 时需管理员)
- 响应：`ArchiveGroup`
- 错误：
  - `400 月份必须在 1-12 之间`
  - `404 指定年月没有文章`

---

### 6) 管理后台

#### GET `/api/admin/stats`（管理员）

- 响应字段：
  - `total_posts`
  - `total_comments`
  - `total_views`
  - `scheduled_posts`
  - `monthly_posts`（最近 6 个月，`[{ month, count }]`）

#### GET `/api/admin/comments`（管理员）

- Query：
  - `skip` (int >= 0, default 0)
  - `limit` (1-100, default 50)
  - `post_id` (int, 可选)
  - `keyword` (string, max 100, 可选)
- 响应：

```json
{
  "comments": [
    {
      "id": 1,
      "post_id": 10,
      "post_title": "文章标题",
      "nickname": "访客",
      "content": "评论内容",
      "parent_id": null,
      "created_at": "2026-02-13T10:00:00Z",
      "updated_at": "2026-02-13T10:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 50
}
```

#### GET `/api/admin/settings`（管理员）

- 响应：

```json
{
  "settings": [
    { "key": "site_title", "value": "Blog AI", "description": "站点标题" }
  ]
}
```

#### POST `/api/admin/settings`（管理员）

- 请求体：

```json
{
  "key": "site_title",
  "value": "Blog AI",
  "description": "站点标题"
}
```

- 允许的 `key`：
  - `comment_rate_limit`
  - `comment_rate_window`
  - `jwt_expire_minutes`
  - `site_title`
  - `site_description`
  - `site_keywords`
  - `comment_enabled`
  - `posts_per_page`
  - `analytics_id`
- 错误：`400 不允许的设置键`

## 常见错误码

- `400 Bad Request`：参数非法（例如月份越界、设置键不允许）
- `401 Unauthorized`：未登录管理员或 token 无效
- `404 Not Found`：文章/评论/归档不存在
- `429 Too Many Requests`：评论频率超限
- `500 Internal Server Error`：服务器内部错误

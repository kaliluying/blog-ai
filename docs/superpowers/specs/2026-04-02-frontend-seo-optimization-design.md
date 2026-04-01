# 前端 SEO 优化设计方案

## 概述

对博客前端进行完整的 SEO 优化，提升搜索引擎收录效果和社交媒体分享体验。

## 网站信息

- **域名**: https://blog.gmlblog.top/
- **站点名称**: 手绘博客

## 优化内容

### 1. 基础 Meta 标签优化

**目标**: 提升搜索引擎收录效果

**实施**：`index.html` 添加基础 Meta 标签
- `title`: 页面标题
- `description`: 页面描述
- `keywords`: 关键词（可选）
- `robots`: 爬虫指令
- `canonical`: 规范 URL

### 2. Open Graph 标签

**目标**: 提升 Facebook、微信等社交平台分享效果

**实施**：`index.html` 和 Article.vue
- `og:title`: 分享标题
- `og:description`: 分享描述
- `og:url`: 页面 URL
- `og:type`: 页面类型（website/article）
- `og:image`: 分享图片（可选）
- `og:site_name`: 站点名称

### 3. Twitter Card 标签

**目标**: 提升 Twitter/X 分享效果

**实施**：`index.html`
- `twitter:card`: 卡片类型
- `twitter:title`: 标题
- `twitter:description`: 描述
- `twitter:image`: 图片（可选）

### 4. JSON-LD 结构化数据

**目标**: 提升 Google 等搜索引擎的理解能力

**实施**：Article.vue 动态注入
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "文章标题",
  "description": "文章摘要",
  "datePublished": "2026-04-01",
  "dateModified": "2026-04-01",
  "author": {
    "@type": "Person",
    "name": "博主大大"
  },
  "publisher": {
    "@type": "Organization",
    "name": "手绘博客",
    "url": "https://blog.gmlblog.top"
  }
}
```

### 5. Sitemap.xml

**目标**: 帮助搜索引擎发现所有页面

**实施**：后端新增 API 端点
- 添加 `/api/sitemap` 返回所有文章 URL 列表
- 前端生成 sitemap.xml

### 6. Robots.txt

**目标**: 控制搜索引擎爬虫行为

**实施**：`frontend/public/robots.txt`
```
User-agent: *
Allow: /
Disallow: /admin/
Sitemap: https://blog.gmlblog.top/sitemap.xml
```

## 涉及文件

| 文件 | 改动类型 |
|------|----------|
| `frontend/index.html` | 修改 |
| `frontend/src/views/Article.vue` | 修改 |
| `frontend/src/views/Home.vue` | 修改 |
| `frontend/src/views/Archive.vue` | 修改 |
| `frontend/src/views/Search.vue` | 修改 |
| `frontend/public/robots.txt` | 创建 |
| `frontend/public/sitemap.xml` | 创建 |
| `backend/main.py` | 修改 |

## 预期效果

- 搜索引擎能正确收录每个文章页面
- 社交媒体分享时显示标题、描述和图片
- Google 能理解文章结构（作者、日期、发布者）
- sitemap 帮助搜索引擎发现所有页面

## 优先级

第二批次（中优先级）

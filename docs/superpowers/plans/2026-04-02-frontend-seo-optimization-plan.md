# 前端 SEO 优化实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完善博客 SEO 功能：Meta 标签、Open Graph、Twitter Card、JSON-LD、sitemap、robots.txt

**Architecture:**
- Meta 标签通过动态更新 document.title 和 meta 元素实现
- JSON-LD 通过动态创建 script 标签注入
- sitemap.xml 和 robots.txt 通过后端 FastAPI 端点服务

**Tech Stack:** Vue 3, FastAPI, Naive UI

**域名:** https://blog.gmlblog.top/

---

## 已知情况

- 后端已有设置系统，支持 `site_title`、`site_description`
- 后端已有 `/api/posts` 返回所有文章列表
- 前端路由：Home(/), Article(/article/:id), Archive(/archive), Search(/search)
- `Article.vue` 在 fetchPost 后有完整文章数据（title, excerpt, date, tags, author）

---

## Chunk 1: 基础 Meta 标签和 Open Graph

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: 更新 index.html 添加 SEO Meta 模板**

将 `index.html` 内容替换为：

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- 基础 Meta -->
    <title>手绘博客</title>
    <meta name="description" content="记录想法，分享技术，热爱生活">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://blog.gmlblog.top/">

    <!-- Open Graph -->
    <meta property="og:title" content="手绘博客">
    <meta property="og:description" content="记录想法，分享技术，热爱生活">
    <meta property="og:url" content="https://blog.gmlblog.top/">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="手绘博客">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="手绘博客">
    <meta name="twitter:description" content="记录想法，分享技术，热爱生活">

    <!-- JSON-LD 占位 -->
    <script type="application/ld+json" id="json-ld"></script>

    <script type="module" src="/src/main.ts"></script>
  </head>
  <body>
    <div id="app"></div>
  </body>
</html>
```

- [ ] **Step 2: 验证**

检查 index.html 是否包含所有必要的 Meta 标签

---

## Chunk 2: Article.vue 动态 Meta 和 JSON-LD

**Files:**
- Modify: `frontend/src/views/Article.vue`

- [ ] **Step 1: 添加 updateSEO 函数**

在 `<script setup>` 中添加：

```typescript
/**
 * 更新页面 SEO Meta 标签
 */
const updateSEO = () => {
  if (!post.value) return

  const title = `${post.value.title} - 手绘博客`
  const description = post.value.excerpt || ''
  const url = `https://blog.gmlblog.top/article/${post.value.id}`

  // 更新 title
  document.title = title

  // 更新 Meta 标签
  const metaMap: Record<string, string> = {
    'description': description,
    'og:title': title,
    'og:description': description,
    'og:url': url,
    'og:type': 'article',
    'twitter:title': title,
    'twitter:description': description,
  }

  Object.entries(metaMap).forEach(([name, content]) => {
    let meta = document.querySelector(`meta[name="${name}"], meta[property="${name}"]`)
    if (!meta) {
      meta = document.createElement('meta')
      if (name.startsWith('og:') || name.startsWith('twitter:')) {
        meta.setAttribute('property', name)
      } else {
        meta.setAttribute('name', name)
      }
      document.head.appendChild(meta)
    }
    meta.setAttribute('content', content)
  })

  // 更新 canonical
  let canonical = document.querySelector('link[rel="canonical"]')
  if (canonical) {
    canonical.setAttribute('href', url)
  }

  // 更新 JSON-LD
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    'headline': post.value.title,
    'description': description,
    'datePublished': post.value.date,
    'dateModified': post.value.updated_at || post.value.date,
    'author': {
      '@type': 'Person',
      'name': '博主大大'
    },
    'publisher': {
      '@type': 'Organization',
      'name': '手绘博客',
      'url': 'https://blog.gmlblog.top/'
    },
    'url': url
  }

  const scriptEl = document.getElementById('json-ld')
  if (scriptEl) {
    scriptEl.textContent = JSON.stringify(jsonLd)
  }
}
```

- [ ] **Step 2: 在 fetchPost 成功后调用 updateSEO**

在 `fetchPost` 函数的 `try` 块中，获取文章成功后调用：

```typescript
// 获取评论
await fetchComments()

// 更新 SEO
updateSEO()

// 等待 DOM 更新后设置代码块复制按钮和目录
await nextTick()
```

- [ ] **Step 3: 验证**

Run: `cd frontend && npm run dev`
检查文章页面是否正确更新 title 和 meta 标签

---

## Chunk 3: Home.vue 动态 Meta

**Files:**
- Modify: `frontend/src/views/Home.vue`

- [ ] **Step 1: 添加 updateSEO 函数**

在 `<script setup>` 中添加：

```typescript
import { onMounted } from 'vue'

/**
 * 更新首页 SEO Meta 标签
 */
const updateSEO = () => {
  const title = '手绘博客 - 首页'
  const description = '记录想法，分享技术，热爱生活'
  const url = 'https://blog.gmlblog.top/'

  document.title = title

  const metaMap: Record<string, string> = {
    'description': description,
    'og:title': title,
    'og:description': description,
    'og:url': url,
    'og:type': 'website',
    'twitter:title': title,
    'twitter:description': description,
  }

  Object.entries(metaMap).forEach(([name, content]) => {
    let meta = document.querySelector(`meta[name="${name}"], meta[property="${name}"]`)
    if (meta) {
      meta.setAttribute('content', content)
    }
  })

  // 清除 JSON-LD（首页不需要 Article 类型）
  const scriptEl = document.getElementById('json-ld')
  if (scriptEl) {
    scriptEl.textContent = ''
  }
}
```

- [ ] **Step 2: 在 onMounted 中调用 updateSEO**

在 `onMounted` 中添加调用：

```typescript
onMounted(() => {
  blogStore.fetchPosts(1, POSTS_PER_PAGE)
  updateSEO()
})
```

- [ ] **Step 3: 验证**

检查首页 title 和 meta 是否正确

---

## Chunk 4: Robots.txt 和 sitemap.xml 端点

**Files:**
- Modify: `backend/main.py`

- [ ] **Step 1: 添加 /robots.txt 端点**

在 `main.py` 中添加：

```python
from fastapi.responses import PlainTextResponse

@app.get("/robots.txt", response_class=PlainTextResponse)
async def get_robots_txt():
    """获取 robots.txt"""
    site_url = os.getenv("SITE_URL", "https://blog.gmlblog.top")
    return f"""User-agent: *
Allow: /
Disallow: /admin/
Sitemap: {site_url}/sitemap.xml

Crawl-delay: 1
"""
```

- [ ] **Step 2: 添加 /sitemap.xml 端点**

在 `main.py` 中添加：

```python
from fastapi.responses import PlainTextResponse

@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def get_sitemap_xml(db: AsyncSession = Depends(get_db)):
    """获取 sitemap.xml"""
    from models import BlogPost
    from sqlalchemy import select

    query = select(BlogPost.id, BlogPost.date, BlogPost.updated_at)
    result = await db.execute(query.order_by(BlogPost.date.desc()))
    posts = result.all()

    site_url = os.getenv("SITE_URL", "https://blog.gmlblog.top")

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # 添加首页
    xml_content += f'  <url>\n    <loc>{site_url}/</loc>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'

    for post in posts:
        url = f"{site_url}/article/{post.id}"
        lastmod = None
        if post.updated_at:
            lastmod = post.updated_at.strftime("%Y-%m-%d")
        elif post.date:
            lastmod = post.date.strftime("%Y-%m-%d")

        priority = "0.9" if post.updated_at else "0.7"

        xml_content += f'  <url>\n    <loc>{url}</loc>\n'
        if lastmod:
            xml_content += f'    <lastmod>{lastmod}</lastmod>\n'
        xml_content += '    <changefreq>monthly</changefreq>\n'
        xml_content += f'    <priority>{priority}</priority>\n'
        xml_content += '  </url>\n'

    xml_content += '</urlset>'
    return xml_content
```

- [ ] **Step 3: 验证**

Run: `curl http://localhost:8000/robots.txt`
Run: `curl http://localhost:8000/sitemap.xml`

---

## Chunk 5: Archive 和 Search 页面 Meta（可选）

**Files:**
- Modify: `frontend/src/views/Archive.vue`
- Modify: `frontend/src/views/Search.vue`

如果需要，可参考 Article.vue 添加 updateSEO 函数。

---

## 执行顺序

1. Chunk 1: 基础 Meta 标签 (index.html)
2. Chunk 2: Article.vue 动态 Meta 和 JSON-LD
3. Chunk 3: Home.vue 动态 Meta
4. Chunk 4: 后端 robots.txt 和 sitemap.xml 端点

---

## 验证命令

```bash
# 后端
cd backend
uv run python main.py &
curl http://localhost:8000/robots.txt
curl http://localhost:8000/sitemap.xml

# 前端
cd frontend
npm run build
npm run dev
```

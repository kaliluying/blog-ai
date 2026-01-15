# Blog AI - 手绘风格个人博客

一个具有手绘风格的个人博客系统，前端使用 Vue 3 + Naive UI + Rough.js 打造独特的视觉体验，后端使用 FastAPI + PostgreSQL 提供高效的 API 服务。

## 特性

- **暗黑模式**: 支持亮色/暗黑/系统自动三种主题模式
- **手绘风格界面**: 使用 Rough.js 生成的独特手绘边框和装饰效果
- **Markdown 支持**: 文章编辑和阅读均支持 Markdown 语法
- **代码高亮与复制**: 文章中的代码块支持语法高亮和一键复制
- **响应式设计**: 适配桌面端和移动端设备
- **管理后台**: 完整的文章管理功能（新建、编辑、删除、搜索）
- **标签系统**: 支持文章标签分类、标签云展示和标签筛选
- **文章归档**: 按年月组织文章，快速浏览历史内容
- **评论系统**: 支持匿名评论、嵌套回复、昵称自动生成
- **阅读量统计**: 记录文章浏览量，支持热门文章排行
- **相关文章推荐**: 基于标签匹配推荐相关文章
- **搜索功能**: 全文搜索文章标题和内容
- **管理员认证**: 简化的密码认证系统

## 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全的 JavaScript 超集
- **Naive UI** - Vue 3 组件库
- **Rough.js** - 手绘风格 SVG 渲染库
- **Pinia** - Vue 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP 客户端
- **DOMPurify** - XSS 防护
- **VueUse** - Vue 3 实用工具库

### 后端
- **FastAPI** - 现代 Python Web 框架
- **SQLAlchemy 2.0** - Python SQL 工具包（异步支持）
- **PostgreSQL** - 关系型数据库
- **asyncpg** - PostgreSQL 异步驱动
- **Alembic** - 数据库迁移工具

## 项目结构

```
blog-ai/
├── frontend/                 # Vue 3 前端项目
│   ├── src/
│   │   ├── api/             # API 接口定义
│   │   ├── components/       # 组件
│   │   │   ├── HandDrawnBorder.vue    # 手绘边框组件
│   │   │   ├── HandDrawnCard.vue      # 手绘卡片组件
│   │   │   ├── HandDrawnIcon.vue      # 手绘图标组件
│   │   │   ├── HandDrawnDivider.vue   # 手绘分割线组件
│   │   │   ├── HandDrawnConfirm.vue   # 手绘确认对话框
│   │   │   ├── HandDrawnBackground.vue# 手绘背景组件
│   │   │   ├── CommentSection.vue     # 评论组件
│   │   │   ├── TableOfContents.vue    # 文章目录组件
│   │   │   ├── RelatedPosts.vue       # 相关文章推荐组件
│   │   │   ├── ArticleSidebar.vue     # 文章侧边栏组件
│   │   │   ├── PopularPosts.vue       # 热门文章组件
│   │   │   ├── PageDecorations.vue    # 页面装饰组件
│   │   │   └── icons/                 # 标准 SVG 图标组件
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia 状态管理
│   │   │   ├── blog.ts       # 文章状态管理
│   │   │   ├── auth.ts       # 认证状态管理
│   │   │   └── theme.ts      # 主题状态管理
│   │   ├── views/            # 页面视图
│   │   │   ├── Home.vue             # 首页
│   │   │   ├── Article.vue          # 文章详情页
│   │   │   ├── Archive.vue          # 文章归档页
│   │   │   ├── ArchiveMonth.vue     # 月度归档页
│   │   │   ├── TagPosts.vue         # 标签文章页
│   │   │   ├── Search.vue           # 搜索结果页
│   │   │   ├── AdminLogin.vue       # 管理员登录页
│   │   │   ├── AdminPosts.vue       # 文章管理页
│   │   │   └── AdminPostNew.vue     # 新建/编辑文章页
│   │   ├── App.vue            # 根组件
│   │   └── main.ts            # 入口文件
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                  # FastAPI 后端项目
│   ├── main.py               # FastAPI 应用入口
│   ├── models.py             # SQLAlchemy 模型
│   ├── schemas.py            # Pydantic 模式
│   ├── crud.py               # 数据库操作
│   ├── database.py           # 数据库连接
│   ├── auth.py               # 管理员认证
│   ├── utils/                # 工具模块
│   │   └── time.py           # 时间工具函数
│   ├── migrations/           # Alembic 迁移脚本
│   │   └── versions/         # 迁移版本
│   ├── pyproject.toml        # Python 依赖配置
│   ├── .env                  # 环境变量配置
│   ├── Dockerfile            # Docker 构建文件
│   └── .dockerignore         # Docker 构建忽略文件
│
├── frontend/                 # Vue 3 前端项目
│   ├── Dockerfile            # Docker 构建文件
│   ├── nginx.conf            # Nginx 配置
│   ├── .dockerignore         # Docker 构建忽略文件
│   └── ...（其他前端文件）
│
├── docker-compose.yml        # Docker Compose 配置
├── CLAUDE.md                 # Claude Code 指导文件
└── README.md                 # 项目说明文档
```

## 快速开始

### 环境要求

- Node.js >= 20.19.0
- Python 3.12+
- PostgreSQL 数据库

### 1. 克隆项目

```bash
git clone https://github.com/kaliluying/blog-ai.git
cd blog-ai
```

### 2. 后端设置

```bash
cd backend

# 安装依赖 (使用 uv 包管理器)
uv sync

# 配置数据库连接
# 编辑 .env 文件
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/blog_ai
# 设置管理员密码: ADMIN_PASSWORD=your_password

# 运行数据库迁移
uv run alembic upgrade head

# 启动服务
uv run python main.py
```

后端服务运行在 http://localhost:8000

### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务运行在 http://localhost:5173

### 4. 构建生产版本

```bash
cd frontend
npm run build
```

### 5. 运行测试

```bash
# 前端测试
cd frontend
npm run test

# 后端测试
cd backend
uv run pytest
```

## Docker 部署（可选）

项目支持使用 Docker Compose 进行容器化部署，包含前端、后端和 PostgreSQL 数据库。

### 环境要求

- Docker Engine >= 20.10
- Docker Compose >= 2.0

### 快速启动

```bash
# 构建并启动所有服务（后台运行）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止所有服务
docker-compose down

# 重新构建镜像并启动
docker-compose up -d --build
```

### 服务端口

| 服务 | 端口 | 描述 |
|------|------|------|
| 前端 | 80 | Nginx 静态资源服务器 |
| 后端 | 8000 | FastAPI 服务 |
| 数据库 | 5432 | PostgreSQL 数据库 |

### 默认配置

- **数据库**: `postgresql://blog:blog_password@localhost:5432/blog`
- **管理员密码**: `admin123`
- **数据持久化**: PostgreSQL 数据存储在 `postgres_data` 卷中

### 目录结构（Docker 相关）

```
blog-ai/
├── docker-compose.yml         # Docker Compose 配置
├── backend/
│   ├── Dockerfile             # 后端镜像构建文件
│   └── .dockerignore          # 后端构建忽略文件
├── frontend/
│   ├── Dockerfile             # 前端镜像构建文件
│   ├── nginx.conf             # Nginx 配置
│   └── .dockerignore          # 前端构建忽略文件
```

## API 接口

### 管理员认证

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/admin/login` | 管理员登录 |
| POST | `/api/admin/logout` | 管理员登出 |

### 文章

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| GET | `/api/posts` | 获取所有文章列表 | 否 |
| GET | `/api/posts/{id}` | 获取单篇文章详情 | 否 |
| GET | `/api/posts/{id}/related` | 获取相关文章推荐 | 否 |
| GET | `/api/posts/count` | 获取文章总数 | 否 |
| GET | `/api/posts/popular` | 获取热门文章排行 | 否 |
| POST | `/api/posts` | 创建新文章 | 管理员 |
| PUT | `/api/posts/{id}` | 更新文章 | 管理员 |
| DELETE | `/api/posts/{id}` | 删除文章 | 管理员 |
| POST | `/api/posts/{id}/view` | 记录文章浏览 | 否 |
| POST | `/api/posts/check-title` | 检查标题是否重复 | 管理员 |
| GET | `/api/search?q=` | 搜索文章 | 否 |

### 归档

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/archive` | 获取所有归档（按年月分组） |
| GET | `/api/archive/{year}` | 获取指定年份归档 |
| GET | `/api/archive/{year}/{month}` | 获取指定年月归档 |

### 评论

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| GET | `/api/posts/{id}/comments` | 获取文章评论 | 否 |
| POST | `/api/comments` | 创建评论（匿名） | 否 |
| DELETE | `/api/comments/{id}` | 删除评论 | 管理员 |

### 请求示例

**管理员登录**
```bash
curl -X POST http://localhost:8000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"password": "admin123"}'
```

**创建文章**
```bash
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "我的第一篇文章",
    "excerpt": "这是文章摘要",
    "content": "这是文章内容，支持 Markdown",
    "tags": ["技术", "生活"]
  }'
```

## 页面路由

| 路径 | 页面 | 描述 |
|------|------|------|
| `/` | Home | 首页，展示文章列表和侧边栏 |
| `/article/:id` | Article | 文章详情页（含目录和评论） |
| `/archive` | Archive | 文章归档页（按年月分组） |
| `/archive/:year/:month` | ArchiveMonth | 月度归档页 |
| `/tag/:tag` | TagPosts | 标签筛选页 |
| `/search` | Search | 搜索结果页 |
| `/admin/login` | AdminLogin | 管理员登录页 |
| `/admin/posts` | AdminPosts | 文章管理页面 |
| `/admin/posts/new` | AdminPostNew | 新建文章页面 |
| `/admin/posts/:id` | AdminPostNew | 编辑文章页面 |

## 主要组件

### HandDrawnBorder
使用 Rough.js 绘制不规则手绘边框，包裹任意内容。

```vue
<HandDrawnBorder :roughness="2" :stroke-width="2">
  <div class="content">你的内容</div>
</HandDrawnBorder>
```

### HandDrawnCard
封装的手绘风格卡片组件。

```vue
<HandDrawnCard title="卡片标题">
  卡片内容
</HandDrawnCard>
```

### HandDrawnIcon
手绘风格图标，支持多种类型。

```vue
<HandDrawnIcon type="star" :size="24" />
```

可用图标类型：`star`、`heart`、`bookmark`、`comment`

### CommentSection
评论组件，支持匿名评论和嵌套回复。

```vue
<CommentSection
  :post-id="postId"
  :comments="comments"
  @refresh="fetchComments"
/>
```

### TableOfContents
文章目录组件，自动提取标题生成目录。

```vue
<TableOfContents :toc="toc" />
```

### RelatedPosts
相关文章推荐组件，基于标签匹配推荐相关文章。

```vue
<RelatedPosts :post-id="post.id" :tags="post.tags" />
```

### ArticleSidebar
文章侧边栏组件，包含博主信息、文章标签和热门文章。

```vue
<ArticleSidebar :tags="post.tags" />
```

### 主题切换
应用支持三种主题模式：亮色、暗色、系统自动。

```typescript
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

// 设置主题
themeStore.setTheme('light')   // 亮色模式
themeStore.setTheme('dark')    // 暗黑模式
themeStore.setTheme('system')  // 系统自动

// 切换主题
themeStore.toggleTheme()
```

## 自定义配置

### 修改 API 地址

编辑 `frontend/.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 修改管理员密码

编辑 `backend/.env` 文件：

```env
ADMIN_PASSWORD=your_password
```

### 修改手绘风格参数

在 `frontend/src/components/HandDrawnBorder.vue` 中调整：

```typescript
const options: rough.Options = {
  roughness: 2,      // 线条粗糙度
  bowing: 1,         // 弯曲程度
  stroke: '#2c3e50', // 边框颜色
  strokeWidth: 2,    // 边框宽度
}
```

## 许可证

MIT License

## 作者

[kaliluying](https://github.com/kaliluying)

## 致谢

- [Vue.js](https://vuejs.org/)
- [Naive UI](https://www.naiveui.com/)
- [Rough.js](https://roughjs.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [VueUse](https://vueuse.org/)
- [Ionicons](https://ionic.io/ionicons) (图标资源)

# Blog AI - 手绘风格个人博客

一个具有手绘风格的个人博客系统，前端使用 Vue 3 + Naive UI + Rough.js，后端使用 FastAPI + PostgreSQL。

## 特性

- 手绘风格界面 (Rough.js)
- 暗黑模式 (亮色/暗黑/系统自动)
- Markdown 文章编辑与渲染
- 代码高亮与一键复制
- 标签系统与文章归档
- 匿名评论与嵌套回复
- 相关文章推荐
- 全文搜索
- 响应式设计

## 快速开始

### 环境要求

- Node.js >= 20.19.0
- Python 3.12+
- PostgreSQL

### 后端

```bash
cd backend
uv sync
# 编辑 .env 配置 DATABASE_URL 和 ADMIN_PASSWORD
uv run alembic upgrade head
uv run python main.py
```

后端运行在 http://localhost:8000

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:5173

## Docker 部署

```bash
docker-compose up -d
```

服务端口：前端 80，后端 8000，数据库 5432

## 技术栈

### 前端
- Vue 3 + TypeScript + Vite
- Naive UI + Rough.js (手绘风格)
- Pinia + Vue Router + Axios
- DOMPurify (XSS 防护) + VueUse

### 后端
- FastAPI + SQLAlchemy 2.0 (异步)
- PostgreSQL + asyncpg
- Alembic (数据库迁移)

## 项目结构

```
blog-ai/
├── frontend/                 # Vue 3 前端项目
│   ├── src/
│   │   ├── api/             # API 接口定义
│   │   │   └── index.ts     # Axios 客户端与类型定义
│   │   ├── components/       # Vue 组件
│   │   │   ├── HandDrawnBackground.vue  # 手绘背景
│   │   │   ├── HandDrawnBorder.vue      # 手绘边框
│   │   │   ├── HandDrawnCard.vue        # 手绘卡片
│   │   │   ├── HandDrawnConfirm.vue     # 手绘确认框
│   │   │   ├── HandDrawnDivider.vue     # 手绘分割线
│   │   │   ├── HandDrawnIcon.vue        # 手绘图标
│   │   │   ├── ArticleSidebar.vue       # 文章侧边栏
│   │   │   ├── CommentSection.vue       # 评论组件
│   │   │   ├── PageDecorations.vue      # 页面装饰
│   │   │   ├── PopularPosts.vue         # 热门文章
│   │   │   ├── RelatedPosts.vue         # 相关文章
│   │   │   ├── TableOfContents.vue      # 文章目录
│   │   │   └── icons/                   # 标准 SVG 图标
│   │   ├── composables/      # 组合式函数
│   │   │   └── useCodeCopy.ts  # 代码复制功能
│   │   ├── router/           # Vue Router 配置
│   │   │   └── index.ts      # 路由定义
│   │   ├── stores/           # Pinia 状态管理
│   │   │   ├── auth.ts       # 认证状态
│   │   │   ├── blog.ts       # 文章状态
│   │   │   └── theme.ts      # 主题状态
│   │   ├── types/            # TypeScript 类型
│   │   │   └── index.ts      # 类型定义
│   │   ├── utils/            # 工具函数
│   │   │   ├── date.ts       # 日期格式化
│   │   │   └── markdown.ts   # Markdown 渲染
│   │   ├── views/            # 页面视图
│   │   │   ├── AdminLogin.vue        # 管理员登录
│   │   │   ├── AdminPostNew.vue      # 新建/编辑文章
│   │   │   ├── AdminPosts.vue        # 文章管理
│   │   │   ├── Archive.vue           # 归档页
│   │   │   ├── ArchiveMonth.vue      # 月度归档
│   │   │   ├── Article.vue           # 文章详情
│   │   │   ├── Home.vue              # 首页
│   │   │   ├── Search.vue            # 搜索页
│   │   │   └── TagPosts.vue          # 标签文章
│   │   ├── App.vue            # 根组件
│   │   └── main.ts            # 入口文件
│   ├── .env                   # 环境变量
│   ├── .eslintrc.cjs          # ESLint 配置
│   ├── index.html             # HTML 模板
│   ├── package.json           # 项目配置
│   ├── tsconfig.json          # TypeScript 配置
│   └── vite.config.ts         # Vite 配置
│
├── backend/                  # FastAPI 后端项目
│   ├── main.py               # FastAPI 应用入口
│   ├── models.py             # SQLAlchemy ORM 模型
│   ├── schemas.py            # Pydantic 模式定义
│   ├── crud.py               # 异步数据库操作
│   ├── database.py           # 数据库连接配置
│   ├── auth.py               # 管理员认证
│   ├── utils/
│   │   └── time.py           # 时间工具函数
│   ├── migrations/           # Alembic 迁移脚本
│   │   ├── env.py            # 迁移环境配置
│   │   └── versions/         # 迁移版本文件
│   ├── .env                  # 环境变量
│   ├── Dockerfile            # Docker 构建文件
│   └── pyproject.toml        # Python 依赖配置
│
├── docker-compose.yml        # Docker Compose 配置
├── CLAUDE.md                 # Claude Code 指导文件
└── README.md                 # 项目说明文档
```

## 许可证

MIT

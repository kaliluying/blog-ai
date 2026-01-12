# Blog AI - 手绘风格个人博客

一个具有手绘风格的个人博客系统，前端使用 Vue 3 + Naive UI + Rough.js 打造独特的视觉体验，后端使用 FastAPI + PostgreSQL 提供高效的 API 服务。

## 特性

- **手绘风格界面**: 使用 Rough.js 生成的独特手绘边框和装饰效果
- **Markdown 支持**: 文章编辑和阅读均支持 Markdown 语法
- **代码高亮与复制**: 文章中的代码块支持语法高亮和一键复制
- **响应式设计**: 适配桌面端和移动端设备
- **管理后台**: 完整的文章管理功能（新建、编辑、删除、搜索）
- **标签系统**: 支持文章标签分类和标签云展示
- **最新文章**: 侧边栏展示最近发布文章

## 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全的 JavaScript 超集
- **Naive UI** - Vue 3 组件库
- **Rough.js** - 手绘风格 SVG 渲染库
- **Pinia** - Vue 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP 客户端

### 后端
- **FastAPI** - 现代 Python Web 框架
- **SQLAlchemy** - Python SQL 工具包
- **PostgreSQL** - 关系型数据库
- **asyncpg** - PostgreSQL 异步驱动

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
│   │   │   └── HandDrawnBackground.vue # 手绘背景组件
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia 状态管理
│   │   ├── views/            # 页面视图
│   │   │   ├── Home.vue             # 首页
│   │   │   ├── Article.vue          # 文章详情页
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
│   └── pyproject.toml        # Python 依赖配置
│
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
# 编辑 main.py 中的 DATABASE_URL

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

## API 接口

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/posts` | 获取所有文章列表 |
| GET | `/api/posts/{id}` | 获取单篇文章详情 |
| POST | `/api/posts` | 创建新文章 |
| PUT | `/api/posts/{id}` | 更新文章 |
| DELETE | `/api/posts/{id}` | 删除文章 |

### 请求示例

**创建文章**
```bash
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
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
| `/article/:id` | Article | 文章详情页 |
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

## 自定义配置

### 修改 API 地址

编辑 `frontend/.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000
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

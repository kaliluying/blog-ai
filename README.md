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

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env  # 编辑 DATABASE_URL 和 ADMIN_PASSWORD

# 运行数据库迁移
uv run alembic upgrade head

# 启动服务
uv run python main.py
```

后端运行在 http://localhost:8000

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 http://localhost:5173

## 命令参考

### 前端

| 命令 | 描述 |
|------|------|
| `npm run dev` | 启动开发服务器 |
| `npm run build` | 构建生产版本 |
| `npm run type-check` | TypeScript 类型检查 |
| `npm run lint` | 代码检查并修复 |
| `npm run format` | 使用 Prettier 格式化代码 |
| `npm run test` | 运行测试 (监听模式) |
| `npm run test:run` | 运行测试一次 |

### 后端

```bash
cd backend

# 启动服务
uv run python main.py

# 运行测试
uv run pytest
uv run pytest tests/test_posts.py -v  # 运行指定测试文件

# 模型变更后生成迁移
uv run alembic revision --autogenerate -m "描述变更"
uv run alembic upgrade head
```

## Docker 部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 重新构建镜像
docker-compose up -d --build
```

**端口**：前端 80，后端 8000，数据库 5432

## 环境变量

### 后端 (backend/.env)

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/blog
ADMIN_PASSWORD=admin123
```

## 技术栈

### 前端
- Vue 3 + TypeScript + Vite
- Naive UI + Rough.js (手绘风格)
- Pinia + Vue Router + Axios
- DOMPurify (XSS 防护) + VueUse
- Vitest (测试)

### 后端
- FastAPI + SQLAlchemy 2.0 (异步)
- PostgreSQL + asyncpg
- Alembic (数据库迁移)
- Pytest (测试)

## 项目结构

```
blog-ai/
├── frontend/                 # Vue 3 前端
│   ├── src/
│   │   ├── api/             # API 接口定义
│   │   ├── components/       # Vue 组件
│   │   │   ├── HandDrawn*   # 手绘风格组件 (Rough.js)
│   │   │   └── icons/       # 标准 SVG 图标
│   │   ├── composables/      # 组合式函数
│   │   ├── router/           # Vue Router 配置
│   │   ├── stores/           # Pinia 状态管理
│   │   ├── types/            # TypeScript 类型
│   │   ├── utils/            # 工具函数
│   │   └── views/            # 页面视图
│   └── ...
│
├── backend/                  # FastAPI 后端
│   ├── main.py              # 应用入口
│   ├── models.py            # SQLAlchemy ORM 模型
│   ├── schemas.py           # Pydantic 模式定义
│   ├── crud.py              # 异步数据库操作
│   ├── database.py          # 数据库连接配置
│   ├── auth.py              # 管理员认证
│   ├── migrations/          # Alembic 迁移脚本
│   └── ...
│
├── docker-compose.yml       # Docker Compose 配置
└── README.md
```

## 许可证

MIT

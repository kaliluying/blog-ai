# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Structure

Monorepo with separate frontend and backend:

```
blog-ai/
├── frontend/                 # Vue 3 + TypeScript + Vite
│   ├── src/
│   │   ├── api/             # API interfaces
│   │   ├── components/       # Vue components (HandDrawn* = Rough.js)
│   │   ├── composables/      # Composables
│   │   ├── router/           # Vue Router config
│   │   ├── stores/           # Pinia stores
│   │   ├── types/            # TypeScript types
│   │   ├── utils/            # Utilities (markdown, date)
│   │   └── views/            # Page views
│   └── ...
│
├── backend/                  # FastAPI + Python
│   ├── main.py              # App entry point
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Async database operations
│   ├── database.py          # DB connection (async aiomysql)
│   ├── auth.py              # Admin authentication
│   └── migrations/          # Alembic migrations
│
├── docker-compose.yml       # Docker deployment
└── CLAUDE.md
```

## Common Commands

### Docker (Recommended for Production)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild images (after code changes)
docker-compose up -d --build
```

### Frontend (Vue 3 + Vite)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Type-check TypeScript
npm run type-check

# Lint code
npm run lint

# Format code
npm run format

# Run tests
npm run test
npm run test:run     # Run tests once (no watch)
```

### Backend (Python + FastAPI)

```bash
cd backend

# Install/update dependencies (requires uv)
uv sync

# Run the application
uv run python main.py

# Run tests
uv run pytest
uv run pytest tests/test_posts.py -v  # Run specific test file
```

**Database**: MySQL 8.4 (not PostgreSQL - migrated)

### Database Migrations (Alembic)

```bash
cd backend

# Generate new migration after model changes
uv run alembic revision --autogenerate -m "描述变更"

# Apply pending migrations
uv run alembic upgrade head

# Downgrade one migration
uv run alembic downgrade -1
```

## Technology Stack

### Frontend
- Vue 3 + TypeScript + Vite
- Naive UI + Rough.js (手绘风格)
- Pinia + Vue Router + Axios
- DOMPurify (XSS 防护) + VueUse
- Vitest (测试)

### Backend
- FastAPI + SQLAlchemy 2.0 (异步)
- MySQL 8.4 + aiomysql (async)
- Alembic (数据库迁移)
- Pytest (测试)

## Security

- **XSS Protection**: All Markdown rendering uses `DOMPurify.sanitize()` with whitelisted tags. Use `renderMarkdownSafe()` or `renderMarkdownWithCodeSafe()` from `utils/markdown.ts`
- **URL Validation**: Links only allow http/https protocols
- **Authentication**: Simple admin password authentication (no JWT). Admin state stored in `auth.ts` store and `localStorage`
- **Comments**: Anonymous comments with nickname stored in `localStorage` for convenience

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/posts` | List posts (?skip=&limit=&include_scheduled=) | No |
| GET | `/api/posts/{id}` | Get single post | No |
| POST | `/api/posts` | Create post | Admin |
| PUT | `/api/posts/{id}` | Update post | Admin |
| DELETE | `/api/posts/{id}` | Delete post | Admin |
| GET | `/api/posts/{id}/related` | Related posts by tags | No |
| GET | `/api/posts/popular` | Popular posts | No |
| POST | `/api/posts/{id}/view` | Record view (IP-limited) | No |
| GET | `/api/search?q=` | Search posts | No |
| GET | `/api/archive` | Archives by year/month | No |
| GET | `/api/posts/{id}/comments` | Get comments (?sort=newest\|oldest) | No |
| POST | `/api/comments` | Create comment (60s rate limit: 5 comments/IP) | No |
| DELETE | `/api/comments/{id}` | Delete comment | Admin |

## Admin Authentication

- Admin login at `/admin/login` with `ADMIN_PASSWORD_HASH` env var (argon2 hash, **not plaintext**)
- Token stored in backend memory and localStorage

## Environment Variables (backend/.env)

```bash
# Database connection
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/blog

# Generate with: openssl rand -hex 32
JWT_SECRET=your_jwt_secret_here

# Generate with: python -c "from pwdlib import PasswordHash; print(PasswordHash.recommended().hash('your_password'))"
ADMIN_PASSWORD_HASH=$argon2id$v=19$...
```

## Frontend Routes

| Path | Component | Description |
|------|-----------|-------------|
| `/` | Home | Article list with pagination |
| `/article/:id` | Article | Article detail with TOC |
| `/archive` | Archive | Articles by year/month |
| `/search` | Search | Search results |
| `/admin/*` | Admin* | Admin pages (guarded) |

## Development Patterns

- **Hand-drawn components**: Prefix with `HandDrawn*` (e.g., `HandDrawnCard.vue`) using Rough.js for SVG rendering
- **Standard icons**: Place in `frontend/src/components/icons/` (plain SVG, no Rough.js)
- **Composables**: Place in `frontend/src/composables/`
- **Memory cleanup**: Return cleanup functions from `init()` methods and call on unmount
- **Debouncing**: Use `useDebounceFn` from `@vueuse/core`
- **Date formatting**: Use `formatDate` and `formatTimeAgo` from `utils/date.ts`
- **Markdown rendering**: Use `renderMarkdownSafe()` or `renderMarkdownWithCodeSafe()` with DOMPurify

## Theme System

Use the theme store for light/dark mode:

```typescript
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

themeStore.setTheme('light')   // Light mode
themeStore.setTheme('dark')    // Dark mode
themeStore.setTheme('system')  // Follow system
themeStore.toggleTheme()       // Toggle between light/dark
```

## Model Changes

After modifying `backend/models.py`, generate migrations:
```bash
uv run alembic revision --autogenerate -m "描述变更"
uv run alembic upgrade head
```
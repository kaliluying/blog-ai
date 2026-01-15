# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Structure

Monorepo with separate frontend and backend:

- `frontend/` - Vue 3 + TypeScript application
- `backend/` - Python FastAPI application

## Common Commands

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
npm run test:ui      # Run tests with UI
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
uv run pytest tests/ -k "test_name"   # Run tests matching pattern
```

### Database Migrations (Alembic)

```bash
cd backend

# Generate new migration after model changes
uv run alembic revision --autogenerate -m "描述变更"

# Apply pending migrations
uv run alembic upgrade head

# Check current migration status
uv run alembic current

# Downgrade one migration
uv run alembic downgrade -1
```

### Admin Authentication

The blog uses a simplified admin authentication system (no JWT, no user registration):
- Admin login at `/admin/login` with password from `ADMIN_PASSWORD` env var
- Session-based tokens generated on login, stored in memory on backend
- Admin routes (`/admin/*`) protected by Vue Router navigation guards
- Token stored in localStorage on frontend

```bash
# Set admin password in backend/.env
ADMIN_PASSWORD=your_password

# Default password: admin123
```

**Database configuration** (in `backend/.env`):
```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/blog
# Migrations use psycopg sync: postgresql://user:password@localhost:5432/blog
```

## Architecture

### Frontend
- **Framework**: Vue 3 with Composition API (`<script setup>`)
- **State Management**: Pinia (store in `src/stores/`)
- **UI Library**: Naive UI + Rough.js for hand-drawn style components
- **Routing**: Vue Router with lazy-loaded routes and admin route guards
- **Path Alias**: `@` maps to `frontend/src/`
- **Pagination**: Frontend and backend both support pagination (?skip=&limit=)

### Backend
- **Framework**: FastAPI with async SQLAlchemy 2.0
- **Database**: PostgreSQL with asyncpg (async) and psycopg (sync migrations)
- **ORM**: SQLAlchemy 2.0 with `Mapped[T]` annotations
- **Validation**: Pydantic v2 with `model_config` and `model_validate()`
- **Migrations**: Alembic (migrations/ directory)

### Data Flow

```
Views -> Pinia Store (blog.ts) -> blogApi (api/index.ts) -> FastAPI Backend
```

### Security
- **XSS Protection**: All Markdown rendering uses `DOMPurify.sanitize()` with whitelisted tags
- **URL Validation**: Links only allow http/https protocols
- **Markdown**: Use `renderMarkdownSafe()` or `renderMarkdownWithCodeSafe()` from `utils/markdown.ts`
- **Authentication**: Simple admin password authentication (no JWT, no user registration). Admin state stored in `auth.ts` store and `localStorage`
- **Comments**: Anonymous comments with nickname stored in `localStorage` for convenience

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/admin/login` | Admin login | No |
| POST | `/api/admin/logout` | Admin logout | No |
| GET | `/api/posts` | List posts (supports ?skip=&limit=) | No |
| GET | `/api/posts/count` | Get total post count | No |
| GET | `/api/posts/{id}` | Get single post | No |
| GET | `/api/posts/{id}/related` | Get related posts by tags | No |
| GET | `/api/posts/popular` | Get popular posts by view count | No |
| POST | `/api/posts` | Create post | Admin |
| PUT | `/api/posts/{id}` | Update post | Admin |
| DELETE | `/api/posts/{id}` | Delete post | Admin |
| POST | `/api/posts/{id}/view` | Record post view (IP-limited) | No |
| GET | `/api/search?q=` | Search posts | No |
| GET | `/api/archive` | All archives by year/month | No |
| GET | `/api/archive/{year}` | Archives by year | No |
| GET | `/api/archive/{year}/{month}` | Archives by year/month | No |
| GET | `/api/posts/{id}/comments` | Get comments | No |
| POST | `/api/comments` | Create anonymous comment | No |
| DELETE | `/api/comments/{id}` | Delete comment | Admin |

## Frontend Routes

| Path | Component | Description |
|------|-----------|-------------|
| `/` | Home | Article list with pagination and sidebar |
| `/article/:id` | Article | Article detail with TOC and code copy |
| `/archive` | Archive | Article archives by year/month |
| `/archive/:year/:month` | ArchiveMonth | Monthly archive |
| `/tag/:tag` | TagPosts | Posts by tag |
| `/search` | Search | Search results |
| `/admin/login` | AdminLogin | Admin login page |
| `/admin/posts` | AdminPosts | Manage articles (table with pagination) |
| `/admin/posts/new` | AdminPostNew | Create article |
| `/admin/posts/:id` | AdminPostNew | Edit article |

## Key Files

- `frontend/src/api/index.ts` - Axios client with all API methods and type definitions
- `frontend/src/stores/blog.ts` - Pinia store for post state with pagination support
- `frontend/src/stores/auth.ts` - Pinia store for admin authentication state
- `frontend/src/stores/theme.ts` - Theme store with light/dark/system mode support
- `frontend/src/views/AdminLogin.vue` - Admin login page with password authentication
- `frontend/src/utils/markdown.ts` - Markdown rendering with XSS protection
- `frontend/src/utils/date.ts` - Shared date formatting utilities
- `frontend/src/components/TableOfContents.vue` - Article TOC with scroll spy
- `frontend/src/components/CommentSection.vue` - Nested anonymous comments component
- `frontend/src/components/RelatedPosts.vue` - Related posts by tags component
- `frontend/src/components/ArticleSidebar.vue` - Sidebar with author info, tags, popular posts
- `frontend/src/components/icons/` - Standard SVG icon components
- `frontend/src/views/Article.vue` - Article detail page
- `backend/main.py` - FastAPI app with all routes
- `backend/models.py` - SQLAlchemy 2.0 ORM models with `Mapped[T]`
- `backend/crud.py` - Async database operations
- `backend/schemas.py` - Pydantic v2 models with `model_config`
- `backend/auth.py` - Admin password authentication utilities
- `backend/database.py` - Database connection with `DeclarativeBase`
- `backend/utils/time.py` - UTC time utilities for timezone-aware datetime
- `backend/migrations/` - Alembic migration scripts

## Development Patterns

- **New components**: Place in `frontend/src/components/` with `HandDrawn*` prefix for hand-drawn style
- **Standard icons**: Place in `frontend/src/components/icons/` (SVG icons without Rough.js)
- **New views**: Place in `frontend/src/views/` and add routes in `frontend/src/router/index.ts`
- **Shared utilities**: Place in `frontend/src/utils/`
- **Composables**: Place in `frontend/src/composables/`
- **Backend utilities**: Place in `backend/utils/`
- **Date formatting**: Use `formatDate` from `utils/date.ts` for consistent formatting
- **Model changes**: Generate migrations with `alembic revision --autogenerate` after modifying `models.py`
- **Comments**: Anonymous comments use `nickname` field, stored in localStorage for convenience
- **Debouncing**: Use `useDebounceFn` from `@vueuse/core` for debounced API calls
- **Memory cleanup**: Return cleanup functions from `init()` methods and call them on unmount

## Tech Stack Notes

- Frontend Node: `^20.19.0 || >=22.12.0`
- Backend Python: 3.12+
- Tags stored as JSON in PostgreSQL `JSON` column (SQLAlchemy 2.0)
- Articles use Markdown content rendered to HTML with custom parser
- Hand-drawn UI components use Rough.js for SVG rendering

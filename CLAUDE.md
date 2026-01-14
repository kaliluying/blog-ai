# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
```

## Architecture

### Frontend
- **Framework**: Vue 3 with Composition API (`<script setup>`)
- **State Management**: Pinia (store in `src/stores/`)
- **UI Library**: Naive UI + Rough.js for hand-drawn style
- **Routing**: Vue Router with lazy-loaded routes
- **Path Alias**: `@` maps to `frontend/src/`

### Backend
- **Framework**: FastAPI with async SQLAlchemy
- **Database**: PostgreSQL with asyncpg driver
- **Package Manager**: uv

### Data Flow

```
Views -> Pinia Store (blog.ts) -> blogApi (api/index.ts) -> FastAPI Backend
```

### Security
- **XSS Protection**: All Markdown rendering uses `DOMPurify.sanitize()` with whitelisted tags
- **URL Validation**: Links only allow http/https protocols
- **Markdown**: Use `renderMarkdownSafe()` or `renderMarkdownWithCodeSafe()` from `utils/markdown.ts`

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/posts` | List all posts | No |
| GET | `/api/posts/{id}` | Get single post | No |
| POST | `/api/posts` | Create post | Admin |
| PUT | `/api/posts/{id}` | Update post | Admin |
| DELETE | `/api/posts/{id}` | Delete post | Admin |
| GET | `/api/search?q=` | Search posts | No |
| GET | `/api/archive` | All archives by year/month | No |
| GET | `/api/archive/{year}` | Archives by year | No |
| GET | `/api/archive/{year}/{month}` | Archives by year/month | No |
| GET | `/api/posts/{id}/comments` | Get comments | No |
| POST | `/api/comments` | Create comment/reply | Yes |
| DELETE | `/api/comments/{id}` | Delete comment | Yes |
| POST | `/api/auth/register` | User register | No |
| POST | `/api/auth/login` | User login | No |
| GET | `/api/auth/me` | Get current user | Yes |

## Frontend Routes

| Path | Component | Description |
|------|-----------|-------------|
| `/` | Home | Article list with sidebar |
| `/article/:id` | Article | Article detail with TOC and code copy |
| `/archive` | Archive | Article archives by year/month |
| `/archive/:year/:month` | ArchiveMonth | Monthly archive |
| `/tag/:tag` | TagPosts | Posts by tag |
| `/search` | Search | Search results |
| `/login` | Login | Login page |
| `/register` | Register | Register page |
| `/admin/posts` | AdminPosts | Manage articles |
| `/admin/posts/new` | AdminPostNew | Create article |
| `/admin/posts/:id` | AdminPostNew | Edit article |

## Key Files

- `frontend/src/api/index.ts` - Axios client with all API methods and type definitions
- `frontend/src/stores/blog.ts` - Pinia store for post state
- `frontend/src/stores/auth.ts` - Pinia store for authentication state
- `frontend/src/utils/markdown.ts` - Markdown rendering with XSS protection
- `frontend/src/utils/date.ts` - Shared date formatting utilities
- `frontend/src/components/TableOfContents.vue` - Article TOC with scroll spy
- `frontend/src/components/CommentSection.vue` - Nested comments component
- `frontend/src/views/Article.vue` - Article detail page
- `backend/main.py` - FastAPI app with all routes
- `backend/crud.py` - Async database operations
- `backend/schemas.py` - Pydantic models for request/response
- `backend/auth.py` - JWT authentication utilities
- `backend/models.py` - SQLAlchemy ORM models

## Tech Stack Notes

- Frontend Node: `^20.19.0 || >=22.12.0`
- Backend Python: 3.12+
- Tags stored as JSON string in PostgreSQL text column
- Articles use Markdown content rendered to HTML with custom parser
- Hand-drawn UI components use Rough.js for SVG rendering

## Development Patterns

- New components go in `frontend/src/components/` with `HandDrawn*` prefix for hand-drawn style
- New views go in `frontend/src/views/` and routes in `frontend/src/router/index.ts`
- Shared utilities go in `frontend/src/utils/`
- Composables go in `frontend/src/composables/`
- Backend utilities go in `backend/utils/`
- Use `formatDate` from `utils/date.ts` for consistent date formatting

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
```

### Backend (Python + FastAPI)

```bash
cd backend

# Install/update dependencies (requires uv)
uv sync

# Run the application
uv run python main.py
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

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts` | List all posts |
| GET | `/api/posts/{id}` | Get single post |
| POST | `/api/posts` | Create post |
| PUT | `/api/posts/{id}` | Update post |
| DELETE | `/api/posts/{id}` | Delete post |

## Frontend Routes

| Path | Component | Description |
|------|-----------|-------------|
| `/` | Home | Article list with sidebar |
| `/article/:id` | Article | Article detail with code copy |
| `/admin/posts` | AdminPosts | Manage articles |
| `/admin/posts/new` | AdminPostNew | Create article |
| `/admin/posts/:id` | AdminPostNew | Edit article |

## Key Files

- `frontend/src/api/index.ts` - Axios client with BlogPost type and blogApi methods
- `frontend/src/stores/blog.ts` - Pinia store for post state
- `frontend/src/utils/markdown.ts` - Markdown rendering with XSS protection
- `backend/main.py` - FastAPI app with routes
- `backend/crud.py` - Async database operations
- `backend/schemas.py` - Pydantic models for request/response

## Tech Stack Notes

- Frontend Node: `^20.19.0 || >=22.12.0`
- Backend Python: 3.12+
- Tags stored as JSON string in PostgreSQL text column

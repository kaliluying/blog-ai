# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is a monorepo with separate frontend and backend directories:

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
- **Framework**: Vue 3 with Composition API
- **State Management**: Pinia (store in `src/stores/`)
- **Build Tool**: Vite
- **TypeScript**: Configured with Vue-specific settings (`tsconfig.app.json`)
- **Path Alias**: `@` is mapped to `frontend/src/`

### Backend
- **Framework**: FastAPI (requires Python 3.12+)
- **Package Manager**: uv
- **Configuration**: `pyproject.toml`

## Tech Stack Notes

- Frontend Node requirement: `^20.19.0 || >=22.12.0`
- Frontend uses ESLint with Vue and TypeScript support
- Frontend uses Prettier for formatting

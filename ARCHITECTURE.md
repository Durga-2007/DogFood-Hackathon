# Architecture

## Overview

DOGFOOD 2026 Portal is a self-hosted hackathon submission and judging portal. It follows a simple, monolithic architecture suitable for a 72-hour hackathon that must run offline with `docker compose up`.

## Component Diagram

```
┌─────────────────────────────────────────┐
│              Docker Container           │
│                                         │
│   ┌────────────────────────────────┐   │
│   │   FastAPI Application           │   │
│   │   (Uvicorn on port 8080)        │   │
│   │                                 │   │
│   │   ┌──────────┐  ┌───────────┐  │   │
│   │   │ API       │  │ HTML      │  │   │
│   │   │ Routers   │  │ Templates │  │   │
│   │   │ /api/*    │  │ Jinja2    │  │   │
│   │   └──────────┘  └───────────┘  │   │
│   │         │                       │   │
│   │   ┌─────▼──────────────────┐   │   │
│   │   │  SQLAlchemy ORM        │   │   │
│   │   └─────────────────────────┘   │   │
│   │         │                       │   │
│   │   ┌─────▼──────────────────┐   │   │
│   │   │  SQLite Database        │   │   │
│   │   │  /app/data/dogfood.db   │   │   │
│   │   └─────────────────────────┘   │   │
│   └────────────────────────────────┘   │
│                                         │
│   Docker Volume: db_data → /app/data   │
└─────────────────────────────────────────┘
```

## Technology Choices

| Concern | Choice | Rationale |
|---------|--------|-----------|
| Language | Python 3.12 | Widely known, stable, fast to prototype |
| Framework | FastAPI | Modern async Python web framework, auto-docs, Pydantic validation |
| Database | SQLite | Zero-config, file-based, no separate service needed |
| ORM | SQLAlchemy 2.0 | Mature, reliable, works with SQLite |
| Templates | Jinja2 | Standard Python templating, simple for server-rendered HTML |
| Container | Docker + Compose | Single command startup |

## Authentication

Bearer token authentication was chosen because:
- No external auth provider
- Simple to implement and understand
- The checker can attach a header directly
- Seed tokens are deterministic and printed on startup

## Authorization

Role-based access control is enforced entirely in the **backend** using FastAPI dependency injection. Every protected route declares its required role via `Depends(require_role(...))`. Frontend UI also hides buttons, but this is supplementary — the API will refuse unauthorized requests even if the frontend is bypassed.

## Seed Process

On startup, `seed.py`:
1. Creates tables (idempotent)
2. Creates 4 deterministic seed users with fixed tokens
3. Loads `fixtures.json`: event → tracks → judges → teams → members → projects → scores
4. Prints auth headers to stdout

The seed is idempotent — running multiple times is safe.

## Directory Layout

```
d:\DogFood1\
├── .dogfood.toml          # Checker configuration
├── acceptance-report.txt  # run.py output (committed after running)
├── docker-compose.yml     # Single service: portal
├── Dockerfile             # Python 3.12-slim
├── entrypoint.sh          # seed.py → uvicorn
├── README.md
├── ARCHITECTURE.md        # This file
├── DATA-MODEL.md
├── JUDGING.md
├── LICENSE
├── data/
│   └── fixtures.json      # Official DOGFOOD fixtures
├── src/
│   ├── main.py            # FastAPI app + HTML routes
│   ├── database.py        # SQLAlchemy engine/session
│   ├── models.py          # ORM models
│   ├── auth.py            # Bearer token auth + role deps
│   ├── seed.py            # Fixture loader + token printer
│   ├── requirements.txt
│   ├── routers/
│   │   ├── auth.py        # POST /api/auth/login|logout, GET /api/auth/me
│   │   ├── events.py      # CRUD /api/events
│   │   ├── teams.py       # CRUD /api/teams
│   │   └── projects.py    # CRUD /api/projects (with deadline enforcement)
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── gallery.html   # Public gallery at /projects
│   │   ├── project_detail.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── events.html
│   │   ├── event_detail.html
│   │   ├── teams.html
│   │   └── submit.html
│   └── static/css/style.css
└── tests/
    └── test_t1.py         # T1 acceptance tests
```

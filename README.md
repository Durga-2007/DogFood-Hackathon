# DOGFOOD 2026 Portal

A self-hosted hackathon submission and judging portal for the DOGFOOD 2026 competition.

## Quick Start

```bash
docker compose up
```

The portal starts at **http://localhost:8080**

The seed script runs automatically on startup. It loads `fixtures.json` and prints auth tokens.

## Demo Accounts

| Role        | Email                      | Password        |
|-------------|---------------------------|-----------------|
| Organizer   | organizer@dogfood.local    | organizer123    |
| Participant | participant@dogfood.local  | participant123  |
| Judge A     | judge_a@dogfood.local      | judge_a123      |
| Judge B     | judge_b@dogfood.local      | judge_b123      |

## Authentication

The application uses **Bearer token authentication**.

Log in at `/api/auth/login` with email/password to receive a token.

Use the token as: `Authorization: Bearer <token>`

Seed tokens are deterministic and printed on startup.

## Key Routes

| Route | Description |
|-------|-------------|
| `GET /projects` | Public gallery (no auth required) |
| `POST /api/projects/submit-new` | Submit a project (participant only, deadline enforced) |
| `POST /api/auth/login` | Login |
| `GET /api/events` | List events |
| `POST /api/events` | Create event (organizer only) |
| `GET /api/teams` | List teams |
| `POST /api/teams` | Create team (participant only) |

## Tech Stack

- **Backend:** Python 3.12 + FastAPI
- **Database:** SQLite (via SQLAlchemy ORM)
- **Templates:** Jinja2
- **Container:** Docker + Docker Compose

## Running Tests

```bash
cd src
pip install -r requirements.txt
pip install pytest httpx
cd ..
pytest tests/
```

## T1 Features

- ✅ Local authentication (email/password → Bearer token)
- ✅ Three roles: Organizer, Participant, Judge
- ✅ Role enforcement in backend (not just frontend)
- ✅ Event creation (organizer only) with tracks
- ✅ Event registration for participants
- ✅ Team creation and joining
- ✅ Project creation with draft/submitted states
- ✅ **Backend deadline enforcement** — POST to closed event returns 422
- ✅ Public project gallery at `/projects` (HTTP 200, no auth)
- ✅ Official fixtures.json loaded on startup (40 projects visible in gallery)
- ✅ `docker compose up` starts a fully working, seeded portal

## Honest Limitations

- No T2 judging/scoring UI yet (score data is seeded for T2)
- No T3/T4 features
- SQLite is not production-grade for concurrent heavy loads (fine for hackathon)

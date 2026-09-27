# Data Model

## Entity-Relationship Overview

```
users ──< auth_tokens
users ──< team_members >── teams
users ──< event_registrations >── events
events ──< tracks
teams >── events
projects >── teams
projects >── tracks
projects >── events
scores >── projects
```

## Tables

### users
| Column | Type | Notes |
|--------|------|-------|
| id | String PK | UUID or seed ID |
| email | String UNIQUE | Login credential |
| name | String | Display name |
| hashed_password | String | SHA-256 of password |
| role | String | `organizer` \| `participant` \| `judge` |
| is_seeded | Boolean | True for fixture-derived rows |

### auth_tokens
| Column | Type | Notes |
|--------|------|-------|
| token | String PK | Random hex 32 bytes |
| user_id | String FK | → users.id |
| created_at | DateTime | UTC |

### events
| Column | Type | Notes |
|--------|------|-------|
| id | String PK | `evt_01` from fixture |
| name | String | Event name |
| description | Text | Optional |
| submissions_close | DateTime | **Official fixture timestamp used as-is** |
| created_by | String FK | → users.id |
| is_seeded | Boolean | |

### tracks
| Column | Type | Notes |
|--------|------|-------|
| id | String PK | `trk_01` … `trk_08` |
| event_id | String FK | → events.id |
| name | String | Track name |

### event_registrations
| Column | Type | Notes |
|--------|------|-------|
| id | String PK | UUID |
| event_id | String FK | → events.id |
| user_id | String FK | → users.id |
| registered_at | DateTime | |

### teams
| Column | Type | Notes |
|--------|------|-------|
| id | String PK | `tm_01` … `tm_40` |
| name | String | Team name |
| event_id | String FK | → events.id |
| is_seeded | Boolean | |

### team_members
| Column | Type | Notes |
|--------|------|-------|
| id | String PK | UUID |
| team_id | String FK | → teams.id |
| user_id | String FK | → users.id (nullable for fixture email-only members) |
| email | String | Member email |

### projects
| Column | Type | Notes |
|--------|------|-------|
| id | String PK | `prj_01` … `prj_41` |
| team_id | String FK | → teams.id |
| track_id | String FK | → tracks.id |
| event_id | String FK | → events.id |
| owner_id | String FK | → users.id |
| title | String | Project title |
| summary | Text | Short description |
| repo_url | String | Repository URL |
| status | String | `draft` \| `submitted` |
| submitted_at | DateTime | Null for drafts |
| is_seeded | Boolean | |

### judge_tracks
| Column | Type | Notes |
|--------|------|-------|
| id | String PK | UUID |
| judge_id | String | Fixture judge ID (e.g. `jdg_01`) |
| track_id | String FK | → tracks.id |
| user_id | String FK | → users.id (linked seed account if applicable) |

### scores
| Column | Type | Notes |
|--------|------|-------|
| id | String PK | UUID |
| judge_fixture_id | String | Fixture judge ID |
| judge_user_id | String FK | → users.id (nullable) |
| project_id | String FK | → projects.id |
| criteria | JSON | `{"functionality": 4, "quality": 3, "innovation": 2}` |
| comment | Text | Judge comment |

## Fixture Mapping

The official `fixtures.json` maps to our schema as follows:

```
fixtures.event          → events row (id, name, submissions_close)
fixtures.tracks[]       → tracks rows (id, name, event_id=evt_01)
fixtures.judges[]       → judge_tracks rows + linked User rows
fixtures.teams[]        → teams rows + team_members rows
fixtures.teams[].members[] → users rows (role=participant, is_seeded=true)
fixtures.projects[]     → projects rows (status=submitted)
fixtures.scores[]       → scores rows (preserved for T2)
```

## Deadline Enforcement

The `submissions_close` from fixtures (`2026-03-01T18:00:00Z`) is stored **as-is** in the database. No substitution is made.

The backend compares `datetime.utcnow()` against `event.submissions_close` on every submission attempt at `POST /api/projects/submit-new` and `POST /api/projects/{id}/submit`. If the current time is >= close time, HTTP 422 is returned.

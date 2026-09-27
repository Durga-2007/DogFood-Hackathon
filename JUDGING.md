# Judging

> **T2 Feature** — This document describes the planned judging system. Judging functionality has not been implemented in T1.

## Planned for T2

### Assignment

Each judge is assigned to one or more tracks (from `fixtures.json` → `judges[].tracks`). The assignment is seeded into the `judge_tracks` table during startup.

Judges will only see projects from their assigned tracks.

### Scoring Criteria

From the fixture data, scores have three criteria:
- `functionality` (1–5)
- `quality` (1–5)
- `innovation` (1–5)

### Planned Routes (T2)

| Route | Description |
|-------|-------------|
| `GET /api/judge/scores` | Judge sees their own submitted scores |
| `GET /api/judge/scores?judge=judge_a` | Returns judge_a's scores (only accessible to judge_a or organizer) |
| `GET /api/export.csv` | Organizer exports all scores as CSV |

### Authorization Rules (T2)

- A judge can only read **their own** scores.
- A judge cannot read another judge's scores (the checker verifies this).
- An organizer can read all scores and export CSV.
- A participant cannot access any judging routes.

### Normalization (Planned)

Score normalization across judges with different rating tendencies is a T2/T3 consideration.

## Current T1 Status

- Score data from fixtures is **seeded into the database** (scores table).
- Judge-track assignments are stored in `judge_tracks`.
- The judge role exists in the system.
- **No judging UI or API endpoints are exposed in T1.**

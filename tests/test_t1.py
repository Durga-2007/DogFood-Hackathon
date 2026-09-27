"""
T1 Tests for the DOGFOOD 2026 portal.
"""
import pytest
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Make src importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Must set DATABASE_URL BEFORE importing app modules
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Use StaticPool so all connections share one in-memory database
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Patch database before importing app
import database
database.engine = test_engine
database.SessionLocal = TestSessionLocal

from database import Base, get_db
from main import app
import main as main_module
import models
from auth import hash_password, make_token
from fastapi.testclient import TestClient

# Override the get_db dependency
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
# Also patch the SessionLocal used directly in main.py HTML routes
main_module.SessionLocal = TestSessionLocal

client = TestClient(app)


@pytest.fixture(autouse=True, scope="function")
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# ── Helpers ───────────────────────────────────────────────────────────────────

def create_user(db, email, name, role, password="password123"):
    user = models.User(
        id=f"test_{email.replace('@','_at_').replace('.','_')}",
        email=email,
        name=name,
        hashed_password=hash_password(password),
        role=role,
    )
    db.add(user)
    db.commit()
    return user


def create_token(db, user):
    token = make_token()
    tok = models.AuthToken(token=token, user_id=user.id)
    db.add(tok)
    db.commit()
    return token


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_event(db, close_future=True, event_id="evt_test"):
    close = (
        datetime.utcnow() + timedelta(days=30) if close_future
        else datetime(2026, 3, 1, 18, 0, 0)  # past date
    )
    event = models.Event(
        id=event_id,
        name="Test Hack 2026",
        submissions_close=close,
    )
    db.add(event)
    db.flush()
    track = models.Track(id="trk_test", event_id=event_id, name="Test Track")
    db.add(track)
    db.commit()
    return event


# ── Authentication ─────────────────────────────────────────────────────────────

class TestAuthentication:
    def test_login_organizer(self, setup_db):
        db = TestSessionLocal()
        create_user(db, "org@test.com", "Organizer", "organizer")
        db.close()
        resp = client.post("/api/auth/login", json={"email": "org@test.com", "password": "password123"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["role"] == "organizer"
        assert "token" in data

    def test_login_participant(self, setup_db):
        db = TestSessionLocal()
        create_user(db, "prt@test.com", "Participant", "participant")
        db.close()
        resp = client.post("/api/auth/login", json={"email": "prt@test.com", "password": "password123"})
        assert resp.status_code == 200
        assert resp.json()["role"] == "participant"

    def test_login_judge(self, setup_db):
        db = TestSessionLocal()
        create_user(db, "jdg@test.com", "Judge", "judge")
        db.close()
        resp = client.post("/api/auth/login", json={"email": "jdg@test.com", "password": "password123"})
        assert resp.status_code == 200
        assert resp.json()["role"] == "judge"

    def test_login_wrong_password(self, setup_db):
        db = TestSessionLocal()
        create_user(db, "org@test.com", "Organizer", "organizer")
        db.close()
        resp = client.post("/api/auth/login", json={"email": "org@test.com", "password": "wrong"})
        assert resp.status_code == 401

    def test_me_endpoint_authenticated(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "me@test.com", "Me", "participant")
        token = create_token(db, user)
        db.close()
        resp = client.get("/api/auth/me", headers=auth_headers(token))
        assert resp.status_code == 200
        assert resp.json()["email"] == "me@test.com"

    def test_me_endpoint_unauthenticated(self, setup_db):
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401


# ── Role Authorization ────────────────────────────────────────────────────────

class TestRoleAuthorization:
    def test_participant_cannot_create_event(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        db.close()
        resp = client.post("/api/events", json={
            "name": "Hack", "submissions_close": "2027-01-01T00:00:00Z"
        }, headers=auth_headers(token))
        assert resp.status_code == 403

    def test_judge_cannot_create_event(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "jdg@test.com", "Jdg", "judge")
        token = create_token(db, user)
        db.close()
        resp = client.post("/api/events", json={
            "name": "Hack", "submissions_close": "2027-01-01T00:00:00Z"
        }, headers=auth_headers(token))
        assert resp.status_code == 403

    def test_organizer_cannot_create_team(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "org@test.com", "Org", "organizer")
        token = create_token(db, user)
        db.close()
        resp = client.post("/api/teams", json={"name": "Team A"}, headers=auth_headers(token))
        assert resp.status_code == 403

    def test_judge_cannot_submit_project(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "jdg@test.com", "Jdg", "judge")
        token = create_token(db, user)
        create_event(db, close_future=True)
        db.close()
        resp = client.post("/api/projects", json={"title": "Test", "event_id": "evt_test"},
                           headers=auth_headers(token))
        assert resp.status_code == 403

    def test_unauthenticated_cannot_create_project(self, setup_db):
        resp = client.post("/api/projects", json={"title": "Test", "event_id": "evt_test"})
        assert resp.status_code in (401, 403)

    def test_protected_routes_require_auth(self, setup_db):
        assert client.post("/api/events", json={"name": "X", "submissions_close": "2027-01-01T00:00:00Z"}).status_code in (401, 403)
        assert client.post("/api/teams", json={"name": "T"}).status_code in (401, 403)


# ── Event Management ──────────────────────────────────────────────────────────

class TestEventManagement:
    def test_organizer_creates_event(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "org@test.com", "Org", "organizer")
        token = create_token(db, user)
        db.close()
        resp = client.post("/api/events", json={
            "name": "My Hackathon",
            "description": "Test",
            "submissions_close": "2027-06-01T18:00:00Z",
            "tracks": [{"name": "Developer Tools"}]
        }, headers=auth_headers(token))
        assert resp.status_code == 201
        assert resp.json()["name"] == "My Hackathon"

    def test_list_events(self, setup_db):
        db = TestSessionLocal()
        create_event(db)
        db.close()
        resp = client.get("/api/events")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_participant_registers_for_event(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        create_event(db)
        db.close()
        resp = client.post("/api/events/evt_test/register", headers=auth_headers(token))
        assert resp.status_code == 201


# ── Team Management ───────────────────────────────────────────────────────────

class TestTeamManagement:
    def test_participant_creates_team(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        create_event(db)
        db.close()
        resp = client.post("/api/teams", json={"name": "Nightshift", "event_id": "evt_test"},
                           headers=auth_headers(token))
        assert resp.status_code == 201
        assert resp.json()["name"] == "Nightshift"

    def test_participant_joins_team(self, setup_db):
        db = TestSessionLocal()
        owner = create_user(db, "owner@test.com", "Owner", "participant")
        joiner = create_user(db, "joiner@test.com", "Joiner", "participant")
        owner_token = create_token(db, owner)
        joiner_token = create_token(db, joiner)
        create_event(db)
        db.close()

        r1 = client.post("/api/teams", json={"name": "Team A", "event_id": "evt_test"},
                         headers=auth_headers(owner_token))
        assert r1.status_code == 201
        team_id = r1.json()["id"]

        r2 = client.post(f"/api/teams/{team_id}/join", headers=auth_headers(joiner_token))
        assert r2.status_code == 200
        assert len(r2.json()["members"]) == 2

    def test_cannot_join_two_teams(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        create_event(db)
        db.close()
        client.post("/api/teams", json={"name": "Team A", "event_id": "evt_test"}, headers=auth_headers(token))
        r2 = client.post("/api/teams", json={"name": "Team B", "event_id": "evt_test"}, headers=auth_headers(token))
        assert r2.status_code == 400


# ── Project Submission ────────────────────────────────────────────────────────

class TestProjectSubmission:
    def test_create_draft(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        create_event(db, close_future=True)
        db.close()
        resp = client.post("/api/projects", json={
            "title": "My Project", "summary": "Does stuff",
            "repo_url": "https://github.com/test", "event_id": "evt_test"
        }, headers=auth_headers(token))
        assert resp.status_code == 201
        assert resp.json()["status"] == "draft"

    def test_edit_draft(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        create_event(db, close_future=True)
        db.close()
        r1 = client.post("/api/projects", json={"title": "Draft", "event_id": "evt_test"}, headers=auth_headers(token))
        proj_id = r1.json()["id"]
        r2 = client.put(f"/api/projects/{proj_id}", json={"title": "Updated"}, headers=auth_headers(token))
        assert r2.status_code == 200
        assert r2.json()["title"] == "Updated"

    def test_final_submit_open_event(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        create_event(db, close_future=True)
        db.close()
        r1 = client.post("/api/projects", json={"title": "Final", "event_id": "evt_test"}, headers=auth_headers(token))
        proj_id = r1.json()["id"]
        r2 = client.post(f"/api/projects/{proj_id}/submit", headers=auth_headers(token))
        assert r2.status_code == 200
        assert r2.json()["status"] == "submitted"

    def test_closed_event_submit_new_rejected(self, setup_db):
        """CRITICAL: Backend must reject submissions to closed events."""
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        create_event(db, close_future=False)  # CLOSED
        db.close()
        resp = client.post("/api/projects/submit-new", json={
            "title": "Late", "event_id": "evt_test"
        }, headers=auth_headers(token))
        assert resp.status_code in (400, 422), f"Backend must reject closed event submissions! Got {resp.status_code}"

    def test_closed_event_finalize_rejected(self, setup_db):
        """Draft finalization must also be rejected for closed event."""
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        create_event(db, close_future=False)  # CLOSED
        db.close()
        r1 = client.post("/api/projects", json={"title": "Draft", "event_id": "evt_test"}, headers=auth_headers(token))
        proj_id = r1.json()["id"]
        r2 = client.post(f"/api/projects/{proj_id}/submit", headers=auth_headers(token))
        assert r2.status_code in (400, 422)


# ── Public Gallery ────────────────────────────────────────────────────────────

class TestPublicGallery:
    def test_gallery_api_no_auth_200(self, setup_db):
        resp = client.get("/api/projects/gallery")
        assert resp.status_code == 200

    def test_gallery_shows_submitted_projects(self, setup_db):
        db = TestSessionLocal()
        ev = create_event(db)
        team = models.Team(id="tm_g1", name="GTeam", event_id=ev.id)
        db.add(team)
        db.flush()
        db.add(models.Project(
            id="prj_g1", team_id="tm_g1", event_id=ev.id,
            title="Glass Signal", summary="Test", status="submitted",
            submitted_at=datetime(2026, 2, 27),
        ))
        db.commit()
        db.close()
        resp = client.get("/api/projects/gallery")
        assert resp.status_code == 200
        assert any(p["title"] == "Glass Signal" for p in resp.json())

    def test_gallery_excludes_drafts(self, setup_db):
        db = TestSessionLocal()
        user = create_user(db, "prt@test.com", "Prt", "participant")
        token = create_token(db, user)
        create_event(db, close_future=True)
        db.close()
        client.post("/api/projects", json={"title": "Secret Draft", "event_id": "evt_test"}, headers=auth_headers(token))
        resp = client.get("/api/projects/gallery")
        assert resp.status_code == 200
        assert not any(p["title"] == "Secret Draft" for p in resp.json())

    def test_fixture_title_in_gallery(self, setup_db):
        """The checker verifies that a known fixture project title appears."""
        db = TestSessionLocal()
        ev = create_event(db)
        team = models.Team(id="tm_f1", name="NorthKiln", event_id=ev.id)
        db.add(team)
        db.flush()
        db.add(models.Project(
            id="prj_01", team_id="tm_f1", event_id=ev.id,
            title="Glass Signal", summary="One line of what it does.",
            repo_url="https://example.org/repo/01", status="submitted",
            submitted_at=datetime(2026, 2, 27), is_seeded=True,
        ))
        db.commit()
        db.close()
        resp = client.get("/api/projects/gallery")
        assert any(p["title"] == "Glass Signal" for p in resp.json())

    def test_project_detail_no_auth(self, setup_db):
        db = TestSessionLocal()
        ev = create_event(db)
        team = models.Team(id="tm_d1", name="DTeam", event_id=ev.id)
        db.add(team)
        db.flush()
        db.add(models.Project(
            id="prj_d1", team_id="tm_d1", event_id=ev.id,
            title="Detail Project", status="submitted",
            submitted_at=datetime(2026, 2, 27),
        ))
        db.commit()
        db.close()
        resp = client.get("/api/projects/prj_d1")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Detail Project"

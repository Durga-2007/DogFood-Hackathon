"""
Main FastAPI application entry point.
"""
import os
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from database import engine, SessionLocal
import models
from models import Base

# Routers
from routers import auth as auth_router
from routers import events as events_router
from routers import teams as teams_router
from routers import projects as projects_router

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DOGFOOD 2026 Portal",
    description="Hackathon submission and judging portal",
    version="1.0.0",
)

# ── Static files and templates ────────────────────────────────────────────────
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ── Register API routers ──────────────────────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(events_router.router)
app.include_router(teams_router.router)
app.include_router(projects_router.router)


def render(request: Request, template: str, context: dict = None):
    """Helper: render Jinja2 template with request (works with old and new Starlette)."""
    ctx = context or {}
    try:
        # New Starlette API
        return templates.TemplateResponse(request=request, name=template, context=ctx)
    except TypeError:
        # Fallback for older Starlette
        ctx["request"] = request
        return templates.TemplateResponse(template, ctx)


# ── HTML page routes ──────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return render(request, "index.html")


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return render(request, "login.html")


@app.get("/projects", response_class=HTMLResponse)
def gallery_page(request: Request):
    """Public gallery page. No auth required. HTTP 200."""
    db = SessionLocal()
    try:
        projects = db.query(models.Project).filter(
            models.Project.status == "submitted"
        ).order_by(models.Project.submitted_at.desc()).all()
        tracks = {t.id: t.name for t in db.query(models.Track).all()}
        teams = {t.id: t.name for t in db.query(models.Team).all()}
        return render(request, "gallery.html", {
            "projects": projects,
            "tracks": tracks,
            "teams": teams,
        })
    finally:
        db.close()


@app.get("/projects/{project_id}", response_class=HTMLResponse)
def project_detail_page(project_id: str, request: Request):
    """Public project detail page. No auth required."""
    db = SessionLocal()
    try:
        p = db.query(models.Project).filter(models.Project.id == project_id).first()
        if not p:
            return HTMLResponse("<h1>Project not found</h1>", status_code=404)
        tracks = {t.id: t.name for t in db.query(models.Track).all()}
        teams = {t.id: t.name for t in db.query(models.Team).all()}
        return render(request, "project_detail.html", {
            "project": p,
            "track_name": tracks.get(p.track_id, ""),
            "team_name": teams.get(p.team_id, ""),
        })
    finally:
        db.close()


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return render(request, "dashboard.html")


@app.get("/events", response_class=HTMLResponse)
def events_page(request: Request):
    return render(request, "events.html")


@app.get("/events/{event_id}", response_class=HTMLResponse)
def event_detail_page(event_id: str, request: Request):
    db = SessionLocal()
    try:
        ev = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not ev:
            return HTMLResponse("<h1>Event not found</h1>", status_code=404)
        return render(request, "event_detail.html", {
            "event": ev,
            "now": datetime.utcnow(),
        })
    finally:
        db.close()


@app.get("/teams", response_class=HTMLResponse)
def teams_page(request: Request):
    return render(request, "teams.html")


@app.get("/submit", response_class=HTMLResponse)
def submit_page(request: Request):
    return render(request, "submit.html")


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "DOGFOOD 2026 Portal"}

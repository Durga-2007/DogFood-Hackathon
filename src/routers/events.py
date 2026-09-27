"""
API router: Events (create, list, detail, register, edit)
"""
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import require_organizer, require_user, get_current_user

router = APIRouter(prefix="/api/events", tags=["events"])


# ── Schemas ──────────────────────────────────────────────────────────────────

class TrackIn(BaseModel):
    id: Optional[str] = None
    name: str


class EventCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    submissions_close: str   # ISO 8601
    tracks: Optional[List[TrackIn]] = []


class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    submissions_close: Optional[str] = None


# ── Routes ───────────────────────────────────────────────────────────────────

@router.get("")
def list_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).all()
    result = []
    for ev in events:
        result.append({
            "id": ev.id,
            "name": ev.name,
            "description": ev.description,
            "submissions_close": ev.submissions_close.isoformat() + "Z",
            "is_open": datetime.utcnow() < ev.submissions_close,
            "tracks": [{"id": t.id, "name": t.name} for t in ev.tracks],
        })
    return result


@router.get("/{event_id}")
def get_event(event_id: str, db: Session = Depends(get_db)):
    ev = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not ev:
        raise HTTPException(404, "Event not found")
    return {
        "id": ev.id,
        "name": ev.name,
        "description": ev.description,
        "submissions_close": ev.submissions_close.isoformat() + "Z",
        "is_open": datetime.utcnow() < ev.submissions_close,
        "tracks": [{"id": t.id, "name": t.name} for t in ev.tracks],
    }


@router.post("", status_code=201)
def create_event(
    body: EventCreate,
    current_user: models.User = Depends(require_organizer),
    db: Session = Depends(get_db),
):
    close_dt = datetime.fromisoformat(
        body.submissions_close.replace("Z", "+00:00")
    ).replace(tzinfo=None)
    event = models.Event(
        id=f"evt_{uuid.uuid4().hex[:8]}",
        name=body.name,
        description=body.description or "",
        submissions_close=close_dt,
        created_by=current_user.id,
    )
    db.add(event)
    db.flush()

    for trk in body.tracks or []:
        track = models.Track(
            id=trk.id or f"trk_{uuid.uuid4().hex[:8]}",
            event_id=event.id,
            name=trk.name,
        )
        db.add(track)

    db.commit()
    db.refresh(event)
    return {"id": event.id, "name": event.name}


@router.put("/{event_id}")
def update_event(
    event_id: str,
    body: EventUpdate,
    current_user: models.User = Depends(require_organizer),
    db: Session = Depends(get_db),
):
    ev = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not ev:
        raise HTTPException(404, "Event not found")
    if body.name is not None:
        ev.name = body.name
    if body.description is not None:
        ev.description = body.description
    if body.submissions_close is not None:
        ev.submissions_close = datetime.fromisoformat(
            body.submissions_close.replace("Z", "+00:00")
        ).replace(tzinfo=None)
    db.commit()
    return {"id": ev.id, "name": ev.name}


@router.post("/{event_id}/register", status_code=201)
def register_for_event(
    event_id: str,
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db),
):
    ev = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not ev:
        raise HTTPException(404, "Event not found")
    existing = db.query(models.EventRegistration).filter(
        models.EventRegistration.event_id == event_id,
        models.EventRegistration.user_id == current_user.id,
    ).first()
    if existing:
        return {"message": "Already registered"}
    reg = models.EventRegistration(event_id=event_id, user_id=current_user.id)
    db.add(reg)
    db.commit()
    return {"message": "Registered successfully"}


@router.post("/{event_id}/tracks", status_code=201)
def add_track(
    event_id: str,
    body: TrackIn,
    current_user: models.User = Depends(require_organizer),
    db: Session = Depends(get_db),
):
    ev = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not ev:
        raise HTTPException(404, "Event not found")
    track = models.Track(
        id=body.id or f"trk_{uuid.uuid4().hex[:8]}",
        event_id=event_id,
        name=body.name,
    )
    db.add(track)
    db.commit()
    return {"id": track.id, "name": track.name}

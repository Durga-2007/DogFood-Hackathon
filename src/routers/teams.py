"""
API router: Teams (create, join, view, manage)
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import require_user, require_participant

router = APIRouter(prefix="/api/teams", tags=["teams"])


class TeamCreate(BaseModel):
    name: str
    event_id: Optional[str] = None


class TeamUpdate(BaseModel):
    name: Optional[str] = None


@router.get("")
def list_teams(
    event_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Team)
    if event_id:
        q = q.filter(models.Team.event_id == event_id)
    teams = q.all()
    return [_team_dict(t) for t in teams]


@router.get("/my")
def my_team(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db),
):
    membership = db.query(models.TeamMember).filter(
        models.TeamMember.user_id == current_user.id
    ).first()
    if not membership:
        return None
    return _team_dict(membership.team)


@router.get("/{team_id}")
def get_team(team_id: str, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(404, "Team not found")
    return _team_dict(team)


@router.post("", status_code=201)
def create_team(
    body: TeamCreate,
    current_user: models.User = Depends(require_participant),
    db: Session = Depends(get_db),
):
    # Check if user is already on a team for this event
    existing = db.query(models.TeamMember).filter(
        models.TeamMember.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(400, "You are already on a team")

    team = models.Team(
        id=f"tm_{uuid.uuid4().hex[:8]}",
        name=body.name,
        event_id=body.event_id,
    )
    db.add(team)
    db.flush()

    member = models.TeamMember(
        team_id=team.id,
        user_id=current_user.id,
        email=current_user.email,
    )
    db.add(member)
    db.commit()
    db.refresh(team)
    return _team_dict(team)


@router.post("/{team_id}/join", status_code=200)
def join_team(
    team_id: str,
    current_user: models.User = Depends(require_participant),
    db: Session = Depends(get_db),
):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(404, "Team not found")

    existing = db.query(models.TeamMember).filter(
        models.TeamMember.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(400, "Already on a team")

    member = models.TeamMember(
        team_id=team_id,
        user_id=current_user.id,
        email=current_user.email,
    )
    db.add(member)
    db.commit()
    return _team_dict(team)


@router.put("/{team_id}")
def update_team(
    team_id: str,
    body: TeamUpdate,
    current_user: models.User = Depends(require_participant),
    db: Session = Depends(get_db),
):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(404, "Team not found")

    # Must be a member
    membership = db.query(models.TeamMember).filter(
        models.TeamMember.team_id == team_id,
        models.TeamMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(403, "Not a member of this team")

    if body.name is not None:
        team.name = body.name
    db.commit()
    return _team_dict(team)


def _team_dict(team: models.Team) -> dict:
    return {
        "id": team.id,
        "name": team.name,
        "event_id": team.event_id,
        "members": [
            {"email": m.email, "user_id": m.user_id}
            for m in team.members
        ],
    }

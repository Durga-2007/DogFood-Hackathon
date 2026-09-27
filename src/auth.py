"""
Authentication and authorization helpers.

Strategy: Bearer token auth.
- Seed script creates deterministic tokens for the four test accounts.
- Regular users get tokens from POST /api/auth/login.
- Token is stored in the auth_tokens table.
- Header format: Authorization: Bearer <token>
"""
import secrets
import hashlib
from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
import models

security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Simple SHA-256 hash. Suitable for a local, self-hosted app."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


def make_token() -> str:
    return secrets.token_hex(32)


def get_user_by_token(token: str, db: Session) -> Optional[models.User]:
    auth = db.query(models.AuthToken).filter(
        models.AuthToken.token == token
    ).first()
    if auth:
        return auth.user
    return None


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[models.User]:
    """Returns user from Bearer token, or None if unauthenticated."""
    if not credentials:
        return None
    return get_user_by_token(credentials.credentials, db)


def require_user(user: Optional[models.User] = Depends(get_current_user)):
    """Require any authenticated user."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user


def require_role(*roles: str):
    """Dependency factory: require user with one of the given roles."""
    def _check(user: models.User = Depends(require_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user.role}' is not authorized for this action",
            )
        return user
    return _check


require_organizer = require_role("organizer")
require_participant = require_role("participant")
require_judge = require_role("judge")
require_organizer_or_participant = require_role("organizer", "participant")

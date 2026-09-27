"""
API router: Authentication (login, logout, current user info)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import verify_password, make_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user_id: str
    role: str
    name: str


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    # Create a new token
    token_value = make_token()
    tok = models.AuthToken(token=token_value, user_id=user.id)
    db.add(tok)
    db.commit()
    return LoginResponse(
        token=token_value,
        user_id=user.id,
        role=user.role,
        name=user.name,
    )


@router.post("/logout")
def logout(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Invalidate all tokens for this user (or just current one)
    if current_user:
        db.query(models.AuthToken).filter(
            models.AuthToken.user_id == current_user.id
        ).delete()
        db.commit()
    return {"message": "Logged out"}


@router.get("/me")
def me(current_user: models.User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
    }

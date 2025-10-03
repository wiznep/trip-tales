from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.database import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
) -> models.User:
    """
    Bypasses authentication for development.
    Retrieves the first user from the database.
    """
    user = crud.user.get(db, id=1)
    if not user:
        # This is a fallback in case you don't have any users in your DB yet.
        # It creates a default user.
        user_in = schemas.UserCreate(
            email="test@example.com", password="password"
        )
        user = crud.user.create(db, obj_in=user_in)
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
# app/api/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.config import settings
from app.crud.user import get_user
from app.database import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = get_user(db, username=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(current_user: User = Depends(get_current_user),) -> User:

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(current_user: User = Depends(get_current_active_user),) -> User:

    if not current_user.is_admin:  # Changed from is_superuser to is_admin
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

def get_current_user_if_pc_chair(current_user: User = Depends(get_current_active_user),) -> User:
    if not any(role.role_type == "PC_CHAIR" for role in current_user.roles):
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have the required PC_CHAIR role",
        )

    return current_user

def get_current_user_if_pc_member(current_user: User = Depends(get_current_active_user),) -> User:

    if not any(role.role_type == "PC_MEMBER" for role in current_user.roles):
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have the required PC_MEMBER role",
        )

    return current_user

def get_current_user_if_author(current_user: User = Depends(get_current_active_user),) -> User:

    if not any(role.role_type == "AUTHOR" for role in current_user.roles):
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have the required AUTHOR role",
        )

    return current_user
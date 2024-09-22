# app/crud/user.py

from sqlalchemy.orm import Session
from app.models.user import User as UserModel  # SQLAlchemy models
from app.schemas.user import UserCreate, User as UserSchema  # Pydantic schemas
from app.schemas.base import RoleType, RoleCreate
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException
from app.models import User as UserModel
from datetime import datetime

def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        is_active=True,
        role=user.role if user.role else RoleType,
        is_admin = True if user.role==RoleType.ADMIN else False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    

    db.add(db_user)

    db.flush()  
       
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def update_user_info(db: Session, username: str, user_update: UserCreate):
    db_user = get_user(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, username: str, old_password: str, new_password: str):
    db_user = get_user(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(old_password, db_user.hashed_password):
        db_user.failed_login_attempts += 1
        if db_user.failed_login_attempts >= 3:
            db_user.is_active = False
        db.commit()
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    db_user.hashed_password = get_password_hash(new_password)
    db_user.failed_login_attempts = 0
    db_user.updated_at = datetime.utcnow()
    db.commit()
    return True

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 3:
            user.is_active = False
        db.commit()
        return False
    user.failed_login_attempts = 0
    user.last_login = datetime.utcnow()
    db.commit()
    return user

# def get_user_roles(db: Session, user_id: int):
#     user = get_user_by_id(db, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user.roles

def assign_role(db: Session, user_id: int, role: RoleCreate):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_role = db.query(RoleModel).filter(
        RoleModel.role_type == role.role_type,
        RoleModel.conference_id == role.conference_id
    ).first()
    
    if not existing_role:
        new_role = RoleModel(role_type=role.role_type, conference_id=role.conference_id)
        db.add(new_role)
        db.flush() 
        existing_role = new_role

    if existing_role not in user.roles:
        user.roles.append(existing_role)
        db.commit()
        return existing_role
    else:
        return existing_role #o idios rolos uparxei idi
    
def delete_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
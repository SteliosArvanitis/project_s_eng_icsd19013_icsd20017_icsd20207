from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud import user as user_crud
from app.schemas.user import User, UserCreate, Token, PasswordUpdate
from app.core.security import create_access_token, get_password_hash
from app.core import deps
from app.database import get_db
from datetime import timedelta
from app.config import settings
from app.models import RoleType as DBUserRole

router = APIRouter()
@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    print ("hello")
    db_user = user_crud.get_user(db, username=user.username)
    print (db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    #db_role = DBUserRole[user.role.value] if user.role else DBUserRole.USER
    #print (db_role)
    return user_crud.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/change-password")
async def change_user_password(
    password_update: PasswordUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    if not user_crud.authenticate_user(db, current_user.username, password_update.old_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    hashed_password = get_password_hash(password_update.new_password)
    user_crud.update_user_password(db,  current_user.username, get_password_hash(password_update.old_password), get_password_hash(password_update.new_password))
    return {"message": "Password updated successfully"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(deps.get_current_active_user)):
    return current_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can delete other users"
        )
    
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account"
        )
    
    success = user_crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"detail": "User successfully deleted"}
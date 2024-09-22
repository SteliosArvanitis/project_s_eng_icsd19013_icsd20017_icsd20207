from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import get_current_user
# from app.models.user import Role
from app.schemas.user import User, UserCreate, UserUpdate, PasswordUpdate
from app.schemas.conference import Conference, ConferenceCreate
from app.schemas.paper import Paper, PaperCreate
import enum

class Role(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


router = APIRouter()

@router.get("/pc_chair_only")
async def pc_chair_endpoint(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.PC_CHAIR:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "Welcome, PC Chair!"}

@router.get("/pc_member_only")
async def pc_member_endpoint(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.PC_MEMBER:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "Welcome, PC Member!"}
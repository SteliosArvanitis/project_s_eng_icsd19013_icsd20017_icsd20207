# app/schemas/conference.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .base import ConferenceBase, Role, PaperBase
from app.schemas.base import ConferenceState
from app.schemas.user import UserBase

class ConferenceCreate(ConferenceBase):
    description: str

class ConferenceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    pc_chairs: Optional[List[int]] = None
    pc_members: Optional[List[int]] = None

class Conference(ConferenceBase):
    id: int
    pc_chairs: List[UserBase]  
    pc_members: List[UserBase] 
    papers: List[PaperBase]

    class Config:
        from_attributes = True

class ConferenceInDB(Conference):
    pass

class ConferencePaperAssignment(BaseModel):
    conference_id: int
    paper_id: int
    reviewer_id: int

class ConferencePaperDecision(BaseModel):
    conference_id: int
    paper_id: int
    decision: str  
    
class ConferenceUserRole(BaseModel):
    conference_id: int
    user_id: int
    role: Role
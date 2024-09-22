# app/schemas/paper.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .base import PaperBase
from app.schemas.user import UserBase

class PaperState(str, Enum):
    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    REVIEWED = "REVIEWED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    ACCEPTED = "ACCEPTED"
    ASSIGNED = "ASSIGNED"

class PaperCreate(PaperBase):
    abstract: str
    content: Optional[str] = None


class PaperUpdate(BaseModel):
    title: Optional[str] = None
    abstract: Optional[str] = None
    content: Optional[str] = None
    authors: Optional[List[int]] = None
    keywords: Optional[List[str]] = None

    class Config:
        from_attributes = True

class Paper(PaperBase):
    id: int
    creation_date: datetime
    state: PaperState
    conference_id: int
    authors: Optional[List[UserBase]]   
    reviewers: Optional[List[UserBase]]  
    reviewer_comments: Optional[str] = None
    reviewer_score: Optional[int] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # metatropi se lista twn keywords
        if obj.keywords:
            obj.keywords = obj.keywords.split(',')
        return super().from_orm(obj)

class PaperInDB(Paper):
    pass

class ReviewCreate(BaseModel):
    paper_id: int
    reviewer_id: int
    comments: str
    score: int

class Review(ReviewCreate):
    id: int
    review_date: datetime

    class Config:
        from_attributes = True
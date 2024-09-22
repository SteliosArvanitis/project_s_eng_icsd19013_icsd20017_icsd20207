from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.database import get_db
from app.models import User
from app.schemas import ConferenceCreate, ConferenceUpdate, Conference
from app.models.conference import ConferenceState

from app.crud import (
    create_conference,
    update_conference,
    add_pc_chairs,
    add_pc_members,
    search_conferences,
    get_conference,
    delete_conference,
    change_conference_state
)
from app.core.deps import get_current_active_user

router = APIRouter()

class PCMembersAdd(BaseModel):
    user_ids: List[int]

class PCChairsAdd(BaseModel):
    user_ids: List[int]

@router.post("/conferences", response_model=Conference)
async def create_new_conference(
    conference: ConferenceCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can create conferences")
    
    new_conference = create_conference(db, conference, current_user)
    return new_conference

@router.put("/conferences/{conference_id}", response_model=Conference)
async def update_conference_endpoint(
    conference_id: int,
    conference_update: ConferenceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can update conferences")
    
    try:
        updated_conference = update_conference(db, conference_id, conference_update, current_user.id)
        return updated_conference
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/conferences/{conference_id}/pc-chairs", response_model=Conference)
async def add_pc_chairs_endpoint(
    conference_id: int,
    user_ids: PCChairsAdd,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can add PC chairs")
    
    try:
        updated_conference = add_pc_chairs(db, conference_id, user_ids.user_ids)
        return updated_conference
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/conferences/{conference_id}/pc-members", response_model=Conference)
async def add_pc_members_endpoint(
    conference_id: int,
    user_ids: PCMembersAdd,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can add PC members")
    
    try:
        updated_conference = add_pc_members(db, conference_id, user_ids.user_ids)
        return updated_conference
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/conferences", response_model=List[Conference])
async def search_conference(
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    conferences = search_conferences(db, name, description, current_user)
    
    return conferences

@router.get("/conferences/{conference_id}", response_model=Conference)
def read_conference(conference_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    db_conference = get_conference(db, conference_id, current_user)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found or you have no rights")
    return db_conference


@router.delete("/conferences/{conference_id}")
def delete_conference_id(
    conference_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        return delete_conference(db, conference_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/conferences/{conference_id}/submit")
async def submit_conference_state(
    conference_id: int,
    
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return change_conference_state(db, conference_id, ConferenceState.CREATED, ConferenceState.SUBMISSION,current_user)

@router.put("/conferences/{conference_id}/assign")
async def assing_conference_state(
    conference_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return change_conference_state(db, conference_id, ConferenceState.SUBMISSION, ConferenceState.ASSIGNMENT, current_user)

# TO ADD

@router.put("/conferences/{conference_id}/review")
async def review_conference_state(
    conference_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return change_conference_state(db, conference_id, ConferenceState.ASSIGNMENT, ConferenceState.REVIEW, current_user)
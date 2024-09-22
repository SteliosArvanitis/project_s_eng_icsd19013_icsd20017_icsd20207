from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import PaperCreate, Paper, PaperUpdate
from app.crud import (
    create_paper,
    update_paper,
    add_co_author,
    change_paper_state
)
from app.core.deps import get_current_active_user
import logging
from app.models.paper import PaperState

router = APIRouter()


@router.post("/conferences/{conference_id}/papers", response_model=Paper)
async def create_new_paper(
    conference_id: int,
    paper: PaperCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    created_paper = create_paper(db, paper, conference_id, current_user.id)
    logging.debug(f"Created paper: {created_paper}")
    logging.debug(f"Paper authors: {created_paper.authors}")
    return created_paper

@router.put("/papers/{paper_id}", response_model=Paper)
async def update_a_paper(
    paper_id: int,
    paper_update: PaperUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated_paper = update_paper(db, paper_id, paper_update, current_user)
    return updated_paper

@router.post("/papers/{paper_id}/add-co-author/{co_author_id}", response_model=Paper)
async def add_paper_co_author(
    paper_id: int,
    co_author_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return add_co_author(db, paper_id, co_author_id, current_user)


@router.put("/papers/{paper_id}/change-state/{new_state}", response_model=Paper)
async def change_a_paper_state(
    paper_id: int,
    new_state: PaperState,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return change_paper_state(db, paper_id, new_state, current_user)
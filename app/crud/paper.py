from fastapi import HTTPException
from pymysql import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime

from app.models import Conference, User, Paper
from app.schemas import PaperCreate, ConferenceUpdate, PaperUpdate
from app.models.paper import PaperState

def create_paper(db: Session, paper: PaperCreate, conference_id: int, creator_id: int):
    #elegxos ean to sunedrio uparxei idi
    conference = db.query(Conference).filter(Conference.id == conference_id).first()
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")

    #elegxos ean uparxei xana to idio paper
    #me ton idio titlo
    existing_paper = db.query(Paper).filter(Paper.title == paper.title, Paper.conference_id == conference_id).first()
    if existing_paper:
        raise HTTPException(status_code=400, detail="A paper with this title already exists in the conference")
   

    #euresi tou xristi apo to id tou
    creator = db.query(User).filter(User.id == creator_id).first()
    if not creator:
        raise HTTPException(status_code=404, detail="Creator user not found")

    #Dimiourgia tou neou paper
    db_paper = Paper(
        title=paper.title,
        abstract=paper.abstract,
        content=paper.content,
        state=PaperState.CREATED,
        creation_date=datetime.utcnow(),
        conference_id=conference_id
    )
    
    print (creator)
    #prosthiki tou xristi ws suggrafea
    db_paper.authors.append(creator)

    #prosthiki tou paper sitn vasi
    db.add(db_paper)

    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating paper")

    # ean o suggrafeas den einai melos tou sunedriou ton vazoume
    if creator not in conference.pc_chairs and creator not in conference.pc_members:
        conference.pc_members.append(creator)

    db.commit()
    db.refresh(db_paper)
    db.refresh(db_paper, attribute_names=['authors'])

    return db_paper

def update_paper(db: Session, paper_id: int, paper_update: PaperUpdate, current_user: User):
    db_paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    print ("autors")
    print (db_paper.authors)
    print (current_user)
    print (current_user not in db_paper.authors)
   
    is_author = any(author.id == current_user.id for author in db_paper.authors)
    
    if not is_author and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have permission to update this paper")

    
    if paper_update.title is not None:
        db_paper.title = paper_update.title
    if paper_update.abstract is not None:
        db_paper.abstract = paper_update.abstract
    if paper_update.content is not None:
        db_paper.content = paper_update.content
    if paper_update.keywords is not None:
        db_paper.set_keywords(paper_update.keywords)


    if paper_update.authors is not None:
        new_authors = db.query(User).filter(User.id.in_(paper_update.authors)).all()
        if len(new_authors) != len(paper_update.authors):
            raise HTTPException(status_code=400, detail="One or more author IDs are invalid")
        db_paper.authors = new_authors

    db.commit()
    db.refresh(db_paper)
    return db_paper

def add_co_author(db: Session, paper_id: int, co_author_id: int, current_user: User):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    co_author = db.query(User).filter(User.id == co_author_id).first()
    if not co_author:
        raise HTTPException(status_code=404, detail="Co-author not found")

    paper.add_co_author(db, current_user, co_author)
    return paper

def change_paper_state(db: Session, paper_id: int, new_state: PaperState, current_user: User):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    paper.change_state(db, new_state, current_user)
    return paper
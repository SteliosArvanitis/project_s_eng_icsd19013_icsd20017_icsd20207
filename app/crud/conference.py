from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime

from app.models import Conference, User
from app.schemas import ConferenceCreate, ConferenceUpdate
from app.models.conference import ConferenceState

def create_conference(db: Session, conference: ConferenceCreate, creator: User) -> Conference:
    db_conference = Conference(
        name=conference.name,
        description=conference.description,
        creation_date=datetime.utcnow(),
        state=ConferenceState.CREATED,
        pc_members=[],
        papers=[]
    )
    # pernaei stin vasi to antikeimeno conference
    db.add(db_conference)
    db.flush()

    creator = db.query(User).filter(User.id == creator.id).first()
    if creator:
        db_conference.pc_chairs.append(creator)


    db.commit()
    db.refresh(db_conference)
    return db_conference


def update_conference(db: Session, conference_id: int, conference_update: ConferenceUpdate, creator_id: int) -> Conference:
    db_conference = db.query(Conference).filter(Conference.id == conference_id).first()
    if not db_conference:
        raise ValueError("Conference not found")

    for key, value in conference_update.dict(exclude_unset=True).items():
        if key not in ['pc_chairs', 'pc_members']:
            setattr(db_conference, key, value)

    # Ανανέωση των pc_chair στο συνέδριο
    if conference_update.pc_chairs:
        creator = db.query(User).filter(User.id == creator_id).first()
        new_pc_chairs = db.query(User).filter(User.id.in_(conference_update.pc_chairs)).all()
        db_conference.pc_chairs = list(set(new_pc_chairs + [creator]))  # Ensure creator remains a PC chair

    # Ανανέωση των pcMember
    if conference_update.pc_members:
        new_pc_members = db.query(User).filter(User.id.in_(conference_update.pc_members)).all()
        db_conference.pc_members = new_pc_members

    db.commit()
    db.refresh(db_conference)
    return db_conference


def search_conferences(db: Session, name: Optional[str] = None, description: Optional[str] = None) -> List[Conference]:
    query = db.query(Conference)
    if name:
        query = query.filter(Conference.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Conference.description.ilike(f"%{description}%"))
    return query.all()

def add_pc_chairs(db: Session, conference_id: int, user_ids: List[int]) -> Conference:
    conference = db.query(Conference).filter(Conference.id == conference_id).first()
    if not conference:
        raise ValueError("Conference not found")

    new_pc_chairs = db.query(User).filter(User.id.in_(user_ids)).all()
    for user in new_pc_chairs:
        if user not in conference.pc_chairs:
            conference.pc_chairs.append(user)

    db.commit()
    db.refresh(conference)
    return conference

def add_pc_members(db: Session, conference_id: int, user_ids: List[int]) -> Conference:
    conference = db.query(Conference).filter(Conference.id == conference_id).first()
    if not conference:
        raise ValueError("Conference not found")

    new_pc_members = db.query(User).filter(User.id.in_(user_ids)).all()
    for user in new_pc_members:
        if user not in conference.pc_members:
            conference.pc_members.append(user)

    db.commit()
    db.refresh(conference)
    return conference

def change_conference_state(db: Session, conference: Conference, new_state: ConferenceState) -> Conference:
    conference.state = new_state
    db.commit()
    db.refresh(conference)
    return conference

def search_conferences(db: Session, name: Optional[str] = None, description: Optional[str] = None, user: Optional[User] = None) -> List[Conference]:
    query = db.query(Conference)

    # ean o xristis zitisei anazitisi me to onoma
    if name:
        name_words = name.split()
        for word in name_words:
            query = query.filter(Conference.name.ilike(f"%{word}%"))

    # ean o xristis zitisei anazitisi me tin perigrafi
    if description:
        desc_words = description.split()
        for word in desc_words:
            query = query.filter(Conference.description.ilike(f"%{word}%"))

    # anazitisi olwn twn sunedriwn
    conferences = query.all()
    
    #analogws ton rolo tou xristi, emfanisi diaforetikwn stoixeiwn
    if user:
        if user.is_admin:
            print ("admin")
            #Oi diaxeiristes mporoun na doune ola ta sunedria
            pass
        else:
            #filtrarisma mono twn sunedriwn pou o xristis einai chair i member
            conferences = [
                conf for conf in conferences 
                if user.is_pc_chair_of(db,conf) or 
                   user.is_pc_member_of(db,conf)
            ]
            print ("filtered")
   
    # Sort conferences by name
    conferences.sort(key=lambda x: x.name)
    print (conferences)
    return conferences

def get_conference(db: Session, conference_id: int,user: Optional[User] = None) -> Conference:
    conference =  db.query(Conference).filter(Conference.id == conference_id).first()
    print (conference)
    if user:
        if user.is_admin:
            print ("admin")
            #Oi diaxeiristes mporoun na doune ola ta sunedria
            return conference
        else:
            if user.is_pc_chair_of(db,conference) or user.is_pc_member_of(db,conference):
                return conference
    print ("nope")

        
def get_conference_view(db: Session, conference_id: int, current_user: User):
    conference = get_conference(db, conference_id)
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")
    is_admin_or_pc_chair = current_user.is_admin or current_user in conference.pc_chairs
    return conference.get_filtered_view(is_admin_or_pc_chair)


def get_conferences(db: Session, skip: int = 0, limit: int = 100,user: Optional[User] = None) -> List[Conference]:
    conferences = db.query(Conference).offset(skip).limit(limit).all()
    if user:
        if user.is_admin:
            print ("admin")
            #Oi diaxeiristes mporoun na doune ola ta sunedria
            pass
        else:
            #filtrarisma mono twn sunedriwn pou o xristis einai chair i member
            conferences = [
                conf for conf in conferences 
                if user.is_pc_chair_of(db,conf) or 
                   user.is_pc_member_of(db,conf)
            ]
            print ("filtered")
    return conferences

def delete_conference(db: Session, conference_id: int, user: User):
    conference = get_conference(db, conference_id, user)
    if not conference:
        raise ValueError("Conference not found or you do not have the rights")
    if user not in conference.pc_chairs and not user.is_admin:
        raise ValueError("Only PC Chairs can delete conferences")
    if conference.state != ConferenceState.CREATED:
        raise ValueError("Conference can only be deleted in CREATED state")
    db.delete(conference)
    db.commit()
    return {"message": "Conference deleted successfully"}

def change_conference_state(db: Session, conference_id: int, old_state: ConferenceState,new_state: ConferenceState, current_user: User):
    conference = get_conference(db, conference_id, current_user)
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")
    if not(current_user.is_admin or current_user.is_pc_chair_of(db,conference) or 
                   current_user.is_pc_member_of(db,conference)):
        raise HTTPException(status_code=403, detail="Only admins or PC chairs can change conference state")

    if conference.state == old_state:
        conference.state = new_state
        db.commit()
        return {"message": f"Conference state changed to {new_state}"}
    else:
        raise HTTPException(status_code=400, detail="Invalid state transition")
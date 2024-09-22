from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Table, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

from app.models.user import User
from .associations import paper_authors, paper_reviewers, conference_pc_chairs, conference_pc_members
from app.models.conference import ConferenceState


class PaperState(str, enum.Enum):
    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    REVIEWED = "REVIEWED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    ACCEPTED = "ACCEPTED"
    ASSIGNED = "ASSIGNED"

class ContentType(str, enum.Enum):
    PDF = "PDF"
    TEX = "TEX"

class PaperRoleType(str, enum.Enum):
    AUTHOR = "AUTHOR"
    REVIEWER= "REVIEWER"

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    abstract = Column(String(1000), nullable=False)
    content = Column(String(255))  # This could be a file path
    content_type = Column(Enum(ContentType))
    state = Column(Enum(PaperState), default=PaperState.CREATED)
    creation_date = Column(DateTime, default=datetime.utcnow)
    submission_date = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    keywords = Column(Text)

    conference_id = Column(Integer, ForeignKey('conferences.id'))

    conference = relationship("Conference", back_populates="papers")
    authors = relationship("User", secondary=paper_authors, back_populates="authored_papers")
    reviewers = relationship("User", secondary=paper_reviewers, back_populates="reviewed_papers")

    reviewer_comments = Column(String(1000), nullable=True)
    reviewer_score = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Paper(id={self.id}, title='{self.title}', state='{self.state}')>"

    def set_keywords(self, keyword_list):
        self.keywords = ','.join(keyword_list) if keyword_list else None

    def get_keywords(self):
        return self.keywords.split(',') if self.keywords else []
    
    def add_co_author(self, db, current_user, co_author):
        is_author = any(author.id == current_user.id for author in self.authors)
        is_coauthor = any(author.id == co_author.id for author in self.authors)

        print (self.authors)
        # #elegxoyme ean o xristis tou aitimatos einai idi siggrafeas tou arthrou
        if not is_author:
            raise HTTPException(status_code=403, detail="Only authors can add co-authors")

        #elegxoyme ean o suggrafeas einai idi siggrafeas tou arthrou
        if is_coauthor:
            raise HTTPException(status_code=400, detail="User is already an author of this paper")

        #prosthiki tou neou suggrafea sto arthro
        self.authors.append(co_author)

        if co_author not in self.conference.pc_chairs and co_author not in self.conference.pc_members:
            self.conference.pc_members.append(co_author)

        db.commit()
        db.refresh(self)

    
    def change_state(self, db, new_state: PaperState, current_user: User):
        # Define valid state transitions
        valid_transitions = {
            PaperState.CREATED: [PaperState.SUBMITTED],
            PaperState.SUBMITTED: [PaperState.ASSIGNED],
            PaperState.ASSIGNED: [PaperState.REVIEWED],
            PaperState.REVIEWED: [PaperState.REJECTED, PaperState.APPROVED],
            PaperState.APPROVED: [PaperState.ACCEPTED],
            # Add more transitions as needed
        }

        if new_state not in valid_transitions.get(self.state, []):
            raise HTTPException(status_code=400, detail=f"Invalid state transition from {self.state} to {new_state}")
        
        
         #elegxoyme ean o xristis tou aitimatos einai siggrafeas tou arthrou
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Only admins can change the state")



        self.state = new_state
        self.last_updated = datetime.utcnow()

        db.commit()
        db.refresh(self)
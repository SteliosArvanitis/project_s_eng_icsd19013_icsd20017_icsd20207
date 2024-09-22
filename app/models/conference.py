from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Table, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum
from .associations import paper_authors, paper_reviewers, conference_pc_chairs, conference_pc_members
from sqlalchemy.orm import Session


class ConferenceRoleType(str, enum.Enum):
    PC_CHAIR = "PC_CHAIR"
    PC_MEMBER = "PC_MEMBER"

class ConferenceState(str, enum.Enum):
    CREATED = "CREATED"
    SUBMISSION = "SUBMISSION"
    ASSIGNMENT = "ASSIGNMENT"
    REVIEW = "REVIEW"
    DECISION = "DECISION"
    FINAL_SUBMISSION = "FINAL_SUBMISSION"
    FINAL = "FINAL"

class Conference(Base):
    __tablename__ = "conferences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(1000))
    state = Column(Enum(ConferenceState), default=ConferenceState.CREATED)
    creation_date = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    papers = relationship("Paper", back_populates="conference")
    pc_chairs = relationship("User", secondary=conference_pc_chairs, back_populates="chaired_conferences")
    pc_members = relationship("User", secondary=conference_pc_members, back_populates="pc_member_conferences")
    #roles = relationship("Role", back_populates="conference")


    def __repr__(self):
        return f"<Conference(id={self.id}, name='{self.name}', state='{self.state}')>"

    @property
    def is_submission_open(self):
        return self.state == ConferenceState.SUBMISSION and \
               (self.submission_deadline is None or datetime.utcnow() < self.submission_deadline)

    @property
    def is_review_open(self):
        return self.state == ConferenceState.REVIEW and \
               (self.review_deadline is None or datetime.utcnow() < self.review_deadline)

    @property
    def is_decision_phase(self):
        return self.state == ConferenceState.DECISION

    @property
    def is_final_submission_open(self):
        return self.state == ConferenceState.FINAL_SUBMISSION and \
               (self.final_submission_deadline is None or datetime.utcnow() < self.final_submission_deadline)

    def can_be_deleted(self):
        return self.state == ConferenceState.CREATED

    # from app.models import User
    # def get_filtered_view(self, db: Session, user: User):
    #     view = {
    #         'id': self.id,
    #         'name': self.name,
    #         'description': self.description,
    #         'state': self.state,
    #         'creation_date': self.creation_date,
    #     }

    #     if user.is_admin or user.is_pc_chair_of(db, self):
    #         view.update({
    #             'last_updated': self.last_updated,
    #             'pc_chairs': [chair.username for chair in self.pc_chairs],
    #             'pc_members': [member.username for member in self.pc_members],
    #         })

    #     return view
from sqlalchemy import Column, Integer,DateTime, String, Boolean, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime
from .associations import paper_authors, paper_reviewers, conference_pc_chairs, conference_pc_members

class RoleType(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role = Column(Enum(RoleType), default=RoleType.USER, nullable=False)
   
    authored_papers = relationship("Paper", secondary=paper_authors, back_populates="authors")
    reviewed_papers = relationship("Paper", secondary=paper_reviewers, back_populates="reviewers")
    chaired_conferences = relationship("Conference", secondary=conference_pc_chairs, back_populates="pc_chairs")
    pc_member_conferences = relationship("Conference", secondary=conference_pc_members, back_populates="pc_members")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    @property
    def is_pc_chair(self):
        return len(self.chaired_conferences) > 0

    @property
    def is_pc_member(self):
        return len(self.pc_member_conferences) > 0

    @property
    def is_author(self):
        return len(self.authored_papers) > 0

    def is_pc_chair_of(self, db, conference):
        from .conference import Conference  # Import here to avoid circular imports
        return db.query(Conference).filter(
            Conference.id == conference.id,
            Conference.pc_chairs.any(id=self.id)
        ).first() is not None

    def is_pc_member_of(self, db, conference):
        from .conference import Conference  # Import here to avoid circular imports
        return db.query(Conference).filter(
            Conference.id == conference.id,
            Conference.pc_members.any(id=self.id)
        ).first() is not None

    def is_author_of(self, paper):
        return paper in self.authored_papers

    def is_reviewer_of(self, paper):
        return paper in self.reviewed_papers

# class Role(Base):
#     __tablename__ = "roles"

#     id = Column(Integer, primary_key=True, index=True)
#     role_type = Column(Enum(RoleType), nullable=False)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     conference_id = Column(Integer, ForeignKey('conferences.id'), nullable=True)

#     users = relationship("User", back_populates="roles")
#     conference = relationship("Conference", back_populates="roles")

#     def __repr__(self):
#         return f"<Role(id={self.id}, role_type='{self.role_type}')>"

# To avoid circular imports, import these at the end of the file
from .paper import Paper
from .conference import Conference
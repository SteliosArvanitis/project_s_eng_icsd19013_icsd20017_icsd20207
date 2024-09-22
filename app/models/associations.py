from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

# user_roles = Table('user_roles', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('role_id', Integer, ForeignKey('roles.id'))
# )

paper_authors = Table('paper_authors', Base.metadata,
    Column('paper_id', Integer, ForeignKey('papers.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

paper_reviewers = Table('paper_reviewers', Base.metadata,
    Column('paper_id', Integer, ForeignKey('papers.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

conference_pc_chairs = Table('conference_pc_chairs', Base.metadata,
    Column('conference_id', Integer, ForeignKey('conferences.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

conference_pc_members = Table('conference_pc_members', Base.metadata,
    Column('conference_id', Integer, ForeignKey('conferences.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


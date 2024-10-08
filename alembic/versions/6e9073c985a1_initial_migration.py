"""Initial migration

Revision ID: 6e9073c985a1
Revises: 
Create Date: 2024-08-21 20:10:25.818718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e9073c985a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conferences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('state', sa.Enum('CREATED', 'SUBMISSION', 'ASSIGNMENT', 'REVIEW', 'DECISION', 'FINAL_SUBMISSION', 'FINAL', name='conferencestate'), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('submission_deadline', sa.DateTime(), nullable=True),
    sa.Column('review_deadline', sa.DateTime(), nullable=True),
    sa.Column('decision_deadline', sa.DateTime(), nullable=True),
    sa.Column('final_submission_deadline', sa.DateTime(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_conferences_id'), 'conferences', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sa.String(length=100), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('failed_login_attempts', sa.Integer(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('conference_pc_chairs',
    sa.Column('conference_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['conference_id'], ['conferences.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('conference_pc_members',
    sa.Column('conference_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['conference_id'], ['conferences.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('papers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('abstract', sa.String(length=1000), nullable=False),
    sa.Column('content', sa.String(length=255), nullable=True),
    sa.Column('content_type', sa.Enum('PDF', 'TEX', name='contenttype'), nullable=True),
    sa.Column('state', sa.Enum('CREATED', 'SUBMITTED', 'REVIEWED', 'REJECTED', 'APPROVED', 'ACCEPTED', name='paperstate'), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('submission_date', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('conference_id', sa.Integer(), nullable=True),
    sa.Column('reviewer_comments', sa.String(length=1000), nullable=True),
    sa.Column('reviewer_score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['conference_id'], ['conferences.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_papers_id'), 'papers', ['id'], unique=False)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_type', sa.Enum('VISITOR', 'USER', 'AUTHOR', 'PC_CHAIR', 'PC_MEMBER', 'ADMIN', name='roletype'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('conference_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['conference_id'], ['conferences.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)
    op.create_table('paper_authors',
    sa.Column('paper_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('paper_reviewers',
    sa.Column('paper_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('user_roles',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('paper_reviewers')
    op.drop_table('paper_authors')
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_papers_id'), table_name='papers')
    op.drop_table('papers')
    op.drop_table('conference_pc_members')
    op.drop_table('conference_pc_chairs')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_conferences_id'), table_name='conferences')
    op.drop_table('conferences')
    # ### end Alembic commands ###

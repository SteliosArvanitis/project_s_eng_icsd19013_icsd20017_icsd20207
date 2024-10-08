"""Update user model and remove role table

Revision ID: 6582dda4136d
Revises: 0ba0fe10fd4f
Create Date: 2024-08-25 22:26:26.673010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '6582dda4136d'
down_revision: Union[str, None] = '0ba0fe10fd4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.add_column('users', sa.Column('role', sa.Enum('USER', 'ADMIN', name='roletype'), nullable=False))
    op.drop_column('users', 'is_admin')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('users', 'role')
    op.create_table('user_roles',
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('role_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='user_roles_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_roles_ibfk_2'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###

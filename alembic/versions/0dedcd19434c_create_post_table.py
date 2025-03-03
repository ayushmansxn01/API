"""create post table

Revision ID: 0dedcd19434c
Revises: 
Create Date: 2024-08-11 16:57:39.291453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dedcd19434c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    , sa.column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass

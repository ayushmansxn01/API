"""add contnt column to  post table

Revision ID: 19e4c0f795d6
Revises: 0dedcd19434c
Create Date: 2024-08-11 17:22:00.008079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19e4c0f795d6'
down_revision: Union[str, None] = '0dedcd19434c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

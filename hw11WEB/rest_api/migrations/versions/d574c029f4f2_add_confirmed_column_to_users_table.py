"""Add confirmed column to users table

Revision ID: d574c029f4f2
Revises: 5089de70b294
Create Date: 2024-05-01 15:10:54.534411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd574c029f4f2'
down_revision: Union[str, None] = '5089de70b294'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

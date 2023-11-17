"""del variables

Revision ID: 785f07a87a1e
Revises: 5c18e7ecf09e
Create Date: 2023-11-17 13:43:13.570847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '785f07a87a1e'
down_revision: Union[str, None] = '5c18e7ecf09e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

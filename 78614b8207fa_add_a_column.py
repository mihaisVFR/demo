"""Add a column

Revision ID: 78614b8207fa
Revises: cfedb280c432
Create Date: 2023-11-21 09:32:49.616198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78614b8207fa'
down_revision: Union[str, None] = 'cfedb280c432'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column('client', sa.Integer))
    op.add_column("clients", sa.Column('user', sa.Integer))


def downgrade() -> None:
    op.drop_column("user", 'client')
    op.drop_column("clients", 'user')

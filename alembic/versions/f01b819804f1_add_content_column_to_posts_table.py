"""add content column to posts table

Revision ID: f01b819804f1
Revises: afe2aa739633
Create Date: 2023-12-12 16:42:18.113800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f01b819804f1'
down_revision: Union[str, None] = 'afe2aa739633'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

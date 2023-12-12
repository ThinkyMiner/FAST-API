"""add users table

Revision ID: 96132758b80d
Revises: f01b819804f1
Create Date: 2023-12-12 16:47:38.623246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96132758b80d'
down_revision: Union[str, None] = 'f01b819804f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email', 'password'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass

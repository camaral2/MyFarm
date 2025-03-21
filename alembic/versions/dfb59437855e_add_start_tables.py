"""add start tables

Revision ID: dfb59437855e
Revises: 
Create Date: 2025-03-17 10:00:39.405925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfb59437855e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('culture',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=False),
                    sa.Column('month_start', sa.Integer, nullable=False, default=0),
                    sa.Column('month_end', sa.Integer, nullable=False, default=0),
                    sa.Column('isActive', sa.Boolean, nullable=False, default=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, default=sa.text("now()")),
                    sa.UniqueConstraint('name'),
                    sa.PrimaryKeyConstraint('id'),
                    if_not_exists=True
                    )
    
    op.create_table('user',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String(length=100), nullable=False),
                    sa.Column('password', sa.String(length=25), nullable=False),
                    sa.Column('isActive', sa.Boolean, nullable=False, default=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, default=sa.text("now()")),
                    sa.UniqueConstraint('email'),
                    sa.PrimaryKeyConstraint('id'),
                    if_not_exists=True
                    )    
    pass


def downgrade() -> None:
    op.drop_table('culture')
    op.drop_table('user')
    pass

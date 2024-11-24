"""Booking: datetime -> date

Revision ID: e4a4523b8bac
Revises: 16dd93c78e6c
Create Date: 2024-11-23 22:12:24.977159

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e4a4523b8bac'
down_revision: Union[str, None] = '16dd93c78e6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('bookings', 'date_from',
                    existing_type=postgresql.TIMESTAMP(),
                    type_=sa.Date(),
                    existing_nullable=False)
    op.alter_column('bookings', 'date_to',
                    existing_type=postgresql.TIMESTAMP(),
                    type_=sa.Date(),
                    existing_nullable=False)


def downgrade() -> None:
    op.alter_column('bookings', 'date_to',
                    existing_type=sa.Date(),
                    type_=postgresql.TIMESTAMP(),
                    existing_nullable=False)
    op.alter_column('bookings', 'date_from',
                    existing_type=sa.Date(),
                    type_=postgresql.TIMESTAMP(),
                    existing_nullable=False)

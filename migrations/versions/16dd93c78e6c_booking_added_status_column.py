"""Booking: added status column

Revision ID: 16dd93c78e6c
Revises: 9c77b0f4ef3c
Create Date: 2024-11-23 20:47:18.205724

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '16dd93c78e6c'
down_revision: Union[str, None] = '9c77b0f4ef3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('bookings', sa.Column('status', sa.Boolean(), server_default='1', nullable=False))


def downgrade() -> None:
    op.drop_column('bookings', 'status')

"""Booking: added time_stamp_mixin

Revision ID: 54071d15b8fb
Revises: e4a4523b8bac
Create Date: 2024-11-24 15:43:52.132744

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '54071d15b8fb'
down_revision: Union[str, None] = 'e4a4523b8bac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('bookings', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('bookings', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))


def downgrade() -> None:
    op.drop_column('bookings', 'updated_at')
    op.drop_column('bookings', 'created_at')

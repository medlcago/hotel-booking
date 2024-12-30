"""delete price_per_day

Revision ID: 68e75a8cc009
Revises: 69cbd94c7348
Create Date: 2024-12-25 10:54:02.700487

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '68e75a8cc009'
down_revision: Union[str, None] = '69cbd94c7348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('bookings', sa.Column('status', sa.String(length=20), server_default='pending', nullable=False))
    op.drop_column('bookings', 'price_per_day')
    op.drop_column('bookings', 'payment_status')


def downgrade() -> None:
    op.add_column('bookings', sa.Column('payment_status', sa.VARCHAR(length=20),
                                        server_default=sa.text("'pending'::character varying"), autoincrement=False,
                                        nullable=False))
    op.add_column('bookings', sa.Column('price_per_day', sa.NUMERIC(), autoincrement=False, nullable=False))
    op.drop_column('bookings', 'status')

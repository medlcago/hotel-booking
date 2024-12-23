"""booking payment_status

Revision ID: 69cbd94c7348
Revises: 54071d15b8fb
Create Date: 2024-12-20 21:15:43.275988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '69cbd94c7348'
down_revision: Union[str, None] = '54071d15b8fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('bookings',
                  sa.Column('payment_status', sa.String(length=20), server_default='pending', nullable=False))
    op.drop_column('bookings', 'status')


def downgrade() -> None:
    op.add_column('bookings', sa.Column('status', sa.Boolean(), server_default='1', nullable=False))
    op.drop_column('bookings', 'payment_status')

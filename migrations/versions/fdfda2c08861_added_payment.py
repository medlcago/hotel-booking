"""added payment

Revision ID: fdfda2c08861
Revises: 68e75a8cc009
Create Date: 2025-02-02 02:47:15.655251

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fdfda2c08861'
down_revision: Union[str, None] = '68e75a8cc009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('payments',
                    sa.Column('payment_id', sa.String(length=100), nullable=False),
                    sa.Column('payment_method', sa.String(length=60), nullable=False),
                    sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
                    sa.Column('currency', sa.String(length=3), nullable=False),
                    sa.Column('booking_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['booking_id'], ['bookings.id'],
                                            name=op.f('fk_payments_booking_id_bookings')),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_payments_user_id_users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_payments'))
                    )


def downgrade() -> None:
    op.drop_table('payments')

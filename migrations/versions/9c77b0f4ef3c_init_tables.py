"""init tables

Revision ID: 9c77b0f4ef3c
Revises: 
Create Date: 2024-11-17 19:48:54.242609

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9c77b0f4ef3c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('hotels',
                    sa.Column('name', sa.String(length=150), nullable=False),
                    sa.Column('location', sa.String(length=300), nullable=False),
                    sa.Column('phone', sa.String(length=20), nullable=True),
                    sa.Column('email', sa.String(length=300), nullable=True),
                    sa.Column('description', sa.String(length=500), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_hotels'))
                    )
    op.create_table('users',
                    sa.Column('first_name', sa.String(length=64), nullable=False),
                    sa.Column('last_name', sa.String(length=64), nullable=False),
                    sa.Column('email', sa.String(length=300), nullable=False),
                    sa.Column('password', sa.String(length=60), nullable=False),
                    sa.Column('phone', sa.String(length=20), nullable=True),
                    sa.Column('date_of_birth', sa.Date(), nullable=True),
                    sa.Column('loyalty_points', sa.Integer(), server_default='0', nullable=False),
                    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
                    sa.Column('is_verified', sa.Boolean(), server_default='0', nullable=False),
                    sa.Column('is_admin', sa.Boolean(), server_default='0', nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
                    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
                    )
    op.create_table('reviews',
                    sa.Column('hotel_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('score', sa.Integer(), nullable=False),
                    sa.Column('comment', sa.String(length=255), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.CheckConstraint('score >= 1 and score <= 5', name=op.f('ck_reviews_rating_score_check')),
                    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], name=op.f('fk_reviews_hotel_id_hotels'),
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_reviews_user_id_users'),
                                            ondelete='SET NULL'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_reviews')),
                    sa.UniqueConstraint('user_id', 'hotel_id', name='rating_user_id')
                    )
    op.create_table('rooms',
                    sa.Column('hotel_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=150), nullable=False),
                    sa.Column('room_type', sa.String(length=32), nullable=False),
                    sa.Column('price_per_day', sa.DECIMAL(precision=10, scale=2), nullable=False),
                    sa.Column('description', sa.String(length=500), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], name=op.f('fk_rooms_hotel_id_hotels'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_rooms'))
                    )
    op.create_table('bookings',
                    sa.Column('room_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('date_from', sa.DateTime(), nullable=False),
                    sa.Column('date_to', sa.DateTime(), nullable=False),
                    sa.Column('price_per_day', sa.Numeric(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], name=op.f('fk_bookings_room_id_rooms')),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_bookings_user_id_users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_bookings'))
                    )


def downgrade() -> None:
    op.drop_table('bookings')
    op.drop_table('rooms')
    op.drop_table('reviews')
    op.drop_table('users')
    op.drop_table('hotels')

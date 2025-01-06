from datetime import date
from typing import Any

from sqlalchemy import select, func, insert, or_, and_, update

from core.db.session import get_session
from enums.status import BookingStatus
from models import Booking
from repositories.base import Repository, Result
from repositories.booking_repo import IBookingRepository

__all__ = ("BookingRepository",)


class BookingRepository(IBookingRepository, Repository[Booking]):
    table = Booking

    async def create_booking(self, values: dict[str, Any]) -> Booking:
        booking_stmt = (
            insert(self.table).
            values(**values).
            returning(self.table)
        )
        async with get_session() as session:
            return await session.scalar(booking_stmt)

    async def update_booking(self, booking_id: int, values: dict[str, Any]) -> Booking | None:
        booking_stmt = (
            update(self.table).
            filter_by(id=booking_id).
            values(**values).
            returning(self.table)
        )
        async with get_session() as session:
            return await session.scalar(booking_stmt)

    async def get_user_bookings(
            self,
            user_id: int,
            limit: int,
            offset: int,
            **kwargs
    ) -> Result[Booking]:
        bookings_stmt = (
            select(self.table).
            filter_by(user_id=user_id, **kwargs).
            limit(limit=limit).
            offset(offset)
        )
        count_stmt = (
            select(func.count(self.table.id)).
            filter_by(user_id=user_id, **kwargs)
        )
        async with get_session() as session:
            bookings = (await session.scalars(bookings_stmt)).all()
            count = await session.scalar(count_stmt)
            return Result(
                count=count,
                items=bookings
            )

    async def get_room_booking(self, room_id: int, date_from: date, date_to: date) -> Booking | None:
        booking_stmt = (
            select(self.table).
            filter_by(room_id=room_id).
            filter(
                or_(
                    and_(
                        self.table.date_from >= date_from,
                        self.table.date_from <= date_to,
                    ),
                    and_(
                        self.table.date_from <= date_from,
                        self.table.date_to > date_from,
                    ),
                ),
                Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed])
            )
        )
        async with get_session() as session:
            return await session.scalar(booking_stmt)

    async def get_user_booking(self, booking_id: int, user_id: int) -> Booking | None:
        booking_stmt = (
            select(self.table).
            filter_by(id=booking_id, user_id=user_id)
        )
        async with get_session() as session:
            return await session.scalar(booking_stmt)

    async def get_booking(self, booking_id: int) -> Booking | None:
        booking_stmt = (
            select(self.table).
            filter_by(id=booking_id)
        )
        async with get_session() as session:
            return await session.scalar(booking_stmt)

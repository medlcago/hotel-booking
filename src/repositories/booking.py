from datetime import date
from typing import Any

from sqlalchemy import select, func, insert, or_, and_, update

from domain.entities import Booking
from domain.repositories import IBookingRepository
from domain.repositories.base import Repository
from enums.status import Status
from schemas.response import PaginationResponse

__all__ = ("BookingRepository",)


class BookingRepository(IBookingRepository, Repository[Booking]):
    table = Booking

    async def create_booking(self, values: dict[str, Any]) -> Booking:
        booking_stmt = (
            insert(self.table).
            values(**values).
            returning(self.table)
        )
        return await self.session.scalar(booking_stmt)

    async def update_status(self, booking_id: int, status: Status) -> Booking | None:
        booking_stmt = (
            update(self.table).
            filter_by(id=booking_id).
            values(status=status).
            returning(self.table)
        )
        return await self.session.scalar(booking_stmt)

    async def get_user_bookings(
            self,
            user_id: int,
            limit: int,
            offset: int,
            **kwargs
    ) -> PaginationResponse[Booking]:
        bookings_stmt = (
            select(self.table).
            filter_by(
                user_id=user_id,
                **kwargs
            ).
            limit(limit=limit).
            offset(offset=offset)
        )
        count_stmt = (
            select(func.count(self.table.id)).
            filter_by(user_id=user_id, **kwargs)
        )
        bookings = (await self.session.scalars(bookings_stmt)).all()
        count = await self.session.scalar(count_stmt)
        return PaginationResponse(
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
                Booking.status.in_([Status.pending, Status.succeeded])
            )
        )
        return await self.session.scalar(booking_stmt)

    async def get_user_booking(self, booking_id: int, user_id: int) -> Booking | None:
        booking_stmt = (
            select(self.table).
            filter_by(
                id=booking_id,
                user_id=user_id
            )
        )
        return await self.session.scalar(booking_stmt)

    async def get_booking(self, booking_id: int) -> Booking | None:
        booking_stmt = (
            select(self.table).
            filter_by(id=booking_id)
        )
        return await self.session.scalar(booking_stmt)

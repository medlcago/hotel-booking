from datetime import date
from typing import Any

from sqlalchemy import insert, select, func, or_, and_, update

from core.db.session import get_session
from domain.entities import Room, Booking
from domain.repositories import IRoomRepository
from domain.repositories.base import Repository
from enums.status import BookingStatus
from schemas.response import PaginationResponse

__all__ = ("RoomRepository",)


class RoomRepository(IRoomRepository, Repository[Room]):
    table = Room

    async def add_room(self, values: dict[str, Any]) -> Room:
        room_stmt = (
            insert(self.table).
            values(**values).
            returning(self.table)
        )
        async with get_session() as session:
            return await session.scalar(room_stmt)

    async def get_room_by_id(self, room_id: int) -> Room | None:
        room_stmt = (
            select(self.table).
            filter_by(id=room_id)
        )
        async with get_session() as session:
            return await session.scalar(room_stmt)

    async def get_rooms(
            self,
            limit: int,
            offset: int,
            date_from: date,
            date_to: date,
            **kwargs
    ) -> PaginationResponse[Room]:
        cte = (
            select(Booking.room_id).
            filter(
                or_(
                    and_(
                        Booking.date_from >= date_from,
                        Booking.date_from <= date_to,
                    ),
                    and_(
                        Booking.date_from <= date_from,
                        Booking.date_to > date_from,
                    ),
                ),
                Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed])
            )
        ).cte("booking_rooms")

        rooms_stmt = (
            select(self.table).
            limit(limit).
            offset(offset).
            filter_by(**kwargs).
            filter(self.table.id.notin_(select(cte.c.room_id)))
        )
        count_stmt = (
            select(func.count(self.table.id)).
            filter_by(**kwargs).
            filter(self.table.id.notin_(select(cte.c.room_id)))
        )
        async with get_session() as session:
            rooms = (await session.scalars(rooms_stmt)).all()
            count = await session.scalar(count_stmt)
            return PaginationResponse(
                count=count,
                items=rooms,
            )

    async def update_room(self, room_id: int, values: dict[str, Any]) -> Room | None:
        room_stmt = (
            update(self.table).
            filter_by(id=room_id).
            values(**values).
            returning(self.table)
        )
        async with get_session() as session:
            return await session.scalar(room_stmt)

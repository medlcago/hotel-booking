from datetime import date
from typing import Any

from sqlalchemy import insert, select, func, or_, and_, update
from sqlalchemy.exc import IntegrityError

from enums.status import BookingStatus
from models import Room, Booking
from repositories.base import Repository, Result, AlreadyExistsError
from repositories.room_repo import IRoomRepository

__all__ = ("RoomRepository",)


class RoomRepository(IRoomRepository, Repository[Room]):
    table = Room

    async def add_room(self, values: dict[str, Any]) -> Room:
        room_stmt = (
            insert(self.table).
            values(**values).
            returning(self.table)
        )
        try:
            return await self.session.scalar(room_stmt)
        except IntegrityError:
            raise AlreadyExistsError

    async def get_room_by_id(self, room_id: int) -> Room | None:
        room_stmt = (
            select(self.table).
            filter_by(id=room_id)
        )
        return await self.session.scalar(room_stmt)

    async def get_rooms(
            self,
            limit: int,
            offset: int,
            date_from: date,
            date_to: date,
            **kwargs
    ) -> Result[Room]:
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

        rooms = (await self.session.scalars(rooms_stmt)).all()
        count = await self.session.scalar(count_stmt)
        return Result(
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
        return await self.session.scalar(room_stmt)

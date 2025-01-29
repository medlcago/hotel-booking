from typing import Any

from sqlalchemy import insert, select, func, update
from sqlalchemy.orm import undefer

from domain.entities import Hotel
from domain.repositories import IHotelRepository
from domain.repositories.base import Repository
from schemas.filters import SortOrder
from schemas.response import PaginationResponse

__all__ = ("HotelRepository",)


class HotelRepository(IHotelRepository, Repository[Hotel]):
    table = Hotel

    async def add_hotel(self, values: dict[str, Any]) -> Hotel:
        hotel_stmt = (
            insert(self.table).
            values(**values).
            returning(self.table)
        )
        return await self.session.scalar(hotel_stmt)

    async def get_hotel_by_id(self, hotel_id: int) -> Hotel | None:
        hotel_stmt = (
            select(self.table).
            filter_by(id=hotel_id).
            options(undefer(self.table.rating))  # noqa
        )
        return await self.session.scalar(hotel_stmt)

    async def get_hotels(
            self,
            limit: int,
            offset: int,
            field: str = "id",
            sort_order: SortOrder = "asc",
            location: str | None = None,
            **kwargs
    ) -> PaginationResponse[Hotel]:
        hotels_stmt = (
            select(self.table).
            limit(limit).
            offset(offset).
            filter_by(**kwargs).
            options(undefer(self.table.rating))  # noqa
        )
        column = getattr(self.table, field, "id")
        hotels_stmt = hotels_stmt.order_by(
            column.desc() if sort_order == "desc" else column.asc()  # noqa
        )
        count_stmt = (
            select(func.count(self.table.id)).
            filter_by(**kwargs)
        )
        if location:
            hotels_stmt = hotels_stmt.filter(self.table.location.ilike(f"%{location}%"))
            count_stmt = count_stmt.filter(self.table.location.ilike(f"%{location}%"))

        hotels = (await self.session.scalars(hotels_stmt)).all()
        count = (await self.session.scalar(count_stmt))
        return PaginationResponse(
            count=count,
            items=hotels,
        )

    async def update_hotel(self, hotel_id: int, values: dict[str, Any]) -> Hotel | None:
        hotel_stmt = (
            update(self.table).
            filter_by(id=hotel_id).
            values(**values).
            returning(self.table)
        )
        return await self.session.scalar(hotel_stmt)

from typing import Any

from sqlalchemy import insert, select, func
from sqlalchemy.orm import selectinload, undefer

from core.types import SortOrderType
from models import Hotel
from repositories.base import Repository, Result


class HotelRepository(Repository[Hotel]):
    table = Hotel

    async def add_hotel(self, values: dict[str, Any]) -> Hotel:
        hotel_stmt = insert(self.table).values(**values).returning(self.table)
        async with self.session_factory() as session:
            hotel = await session.scalar(hotel_stmt)
            return hotel

    async def get_hotel_by_id(self, hotel_id: int) -> Hotel | None:
        hotel_stmt = (
            select(self.table).
            filter_by(id=hotel_id).
            options(selectinload(self.table.rooms), undefer(self.table.rating))  # noqa
        )
        async with self.session_factory() as session:
            return await session.scalar(hotel_stmt)

    async def get_hotels(
            self,
            limit: int,
            offset: int,
            field: str = "id",
            sort_order: SortOrderType = "asc",
            location: str | None = None,
            **kwargs
    ) -> Result[Hotel]:
        hotels_stmt = (
            select(self.table).
            limit(limit).
            offset(offset).
            filter_by(**kwargs).
            options(undefer(self.table.rating))  # noqa
        )
        if column := getattr(self.table, field, None):
            hotels_stmt = hotels_stmt.order_by(
                column.desc() if sort_order == "desc" else column.asc()  # noqa
            )
        count_stmt = select(func.count(self.table.id)).filter_by(**kwargs)
        if location:
            hotels_stmt = hotels_stmt.filter(self.table.location.ilike(f"%{location}%"))
            count_stmt = count_stmt.filter(self.table.location.ilike(f"%{location}%"))

        async with self.session_factory() as session:
            hotels = (await session.scalars(hotels_stmt)).all()
            count = (await session.scalar(count_stmt))
            return Result(
                count=count,
                items=hotels,
            )

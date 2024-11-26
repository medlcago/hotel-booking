from typing import Protocol, Any

from core.types import SortOrderType
from models import Hotel
from repositories.base import Result
from .hotel_repo import HotelRepository


class IHotelRepository(Protocol):
    async def add_hotel(self, values: dict[str, Any]) -> Hotel:
        ...

    async def get_hotel_by_id(self, hotel_id: int) -> Hotel | None:
        ...

    async def get_hotels(
            self,
            limit: int,
            offset: int,
            field: str = "id",
            sort_order: SortOrderType = "asc",
            location: str | None = None,
            **kwargs
    ) -> Result[Hotel]:
        ...

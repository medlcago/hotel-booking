from abc import ABC
from typing import Any

from models import Hotel
from repositories.base import Result
from schemas.filters import SortOrderType


class IHotelRepository(ABC):
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

    async def update_hotel(self, hotel_id: int, values: dict[str, Any]) -> Hotel | None:
        ...

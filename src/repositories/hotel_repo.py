from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Hotel
    from repositories.base import Result
    from schemas.filters import SortOrderType


class IHotelRepository(ABC):
    @abstractmethod
    async def add_hotel(self, values: dict[str, Any]) -> Hotel:
        raise NotImplementedError

    @abstractmethod
    async def get_hotel_by_id(self, hotel_id: int) -> Hotel | None:
        raise NotImplementedError

    @abstractmethod
    async def get_hotels(
            self,
            limit: int,
            offset: int,
            field: str = "id",
            sort_order: SortOrderType = "asc",
            location: str | None = None,
            **kwargs
    ) -> Result[Hotel]:
        raise NotImplementedError

    @abstractmethod
    async def update_hotel(self, hotel_id: int, values: dict[str, Any]) -> Hotel | None:
        raise NotImplementedError

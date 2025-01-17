from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.hotel import (
        HotelCreateRequest,
        HotelResponse,
        HotelCreateResponse,
        HotelParams,
        HotelUpdate
    )
    from schemas.response import PaginationResponse


class IHotelService(ABC):
    @abstractmethod
    async def add_hotel(self, schema: HotelCreateRequest) -> HotelCreateResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_hotel_by_id(self, hotel_id: int) -> HotelResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_hotels(self, params: HotelParams) -> PaginationResponse[HotelResponse]:
        raise NotImplementedError

    @abstractmethod
    async def update_hotel(self, hotel_id: int, schema: HotelUpdate) -> HotelUpdate:
        raise NotImplementedError

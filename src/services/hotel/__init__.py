from typing import Protocol

from schemas.hotel import (
    HotelCreateRequest,
    HotelResponse,
    HotelCreateResponse,
    HotelParams,
    HotelUpdate
)
from schemas.pagination import PaginationResponse
from .hotel_service import HotelService


class IHotelService(Protocol):
    async def add_hotel(self, schema: HotelCreateRequest) -> HotelCreateResponse:
        ...

    async def get_hotel_by_id(self, hotel_id: int) -> HotelResponse:
        ...

    async def get_hotels(self, params: HotelParams) -> PaginationResponse[HotelResponse]:
        ...

    async def update_hotel(self, hotel_id: int, schema: HotelUpdate) -> HotelUpdate:
        ...

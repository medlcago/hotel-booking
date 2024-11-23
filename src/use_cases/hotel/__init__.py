from typing import Protocol

from schemas.hotel import HotelCreateRequest, HotelResponse, HotelCreateResponse, HotelParams
from schemas.pagination import PaginationResponse
from .hotel_use_case import HotelUseCase


class IHotelUseCase(Protocol):
    async def add_hotel(self, schema: HotelCreateRequest) -> HotelCreateResponse:
        ...

    async def get_hotel_by_id(self, hotel_id: int) -> HotelResponse:
        ...

    async def get_hotels(self, params: HotelParams) -> PaginationResponse[HotelResponse]:
        ...

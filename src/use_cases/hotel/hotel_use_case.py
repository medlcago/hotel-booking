from dataclasses import dataclass

from schemas.hotel import (
    HotelCreateRequest,
    HotelResponse,
    HotelCreateResponse,
    HotelParams,
    HotelUpdate
)
from schemas.pagination import PaginationResponse
from services.hotel import IHotelService


@dataclass(frozen=True, slots=True)
class HotelUseCase:
    hotel_service: IHotelService

    async def add_hotel(self, schema: HotelCreateRequest) -> HotelCreateResponse:
        hotel = await self.hotel_service.add_hotel(schema=schema)
        return hotel

    async def get_hotel_by_id(self, hotel_id: int) -> HotelResponse:
        hotel = await self.hotel_service.get_hotel_by_id(hotel_id=hotel_id)
        return hotel

    async def get_hotels(self, params: HotelParams) -> PaginationResponse[HotelResponse]:
        hotels = await self.hotel_service.get_hotels(params=params)
        return hotels

    async def update_hotel(self, hotel_id: int, schema: HotelUpdate) -> HotelUpdate:
        hotel = await self.hotel_service.update_hotel(hotel_id=hotel_id, schema=schema)
        return hotel

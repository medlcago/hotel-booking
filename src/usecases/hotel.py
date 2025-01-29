from dataclasses import dataclass

from core.db.transactional import Transactional
from domain.services import IHotelService
from domain.usecases import IHotelUseCase
from schemas.hotel import HotelCreateRequest, HotelResponse, HotelParams, HotelUpdate, HotelCreateResponse
from schemas.response import PaginationResponse

__all__ = ("HotelUseCase",)


@dataclass(frozen=True, slots=True)
class HotelUseCase(IHotelUseCase):
    hotel_service: IHotelService

    @Transactional()
    async def add_hotel(self, schema: HotelCreateRequest) -> HotelCreateResponse:
        return await self.hotel_service.add_hotel(schema=schema)

    async def get_hotel_by_id(self, hotel_id: int) -> HotelResponse:
        return await self.hotel_service.get_hotel_by_id(hotel_id=hotel_id)

    async def get_hotels(self, params: HotelParams) -> PaginationResponse[HotelResponse]:
        return await self.hotel_service.get_hotels(params=params)

    @Transactional()
    async def update_hotel(self, hotel_id: int, schema: HotelUpdate) -> HotelUpdate:
        return await self.hotel_service.update_hotel(hotel_id=hotel_id, schema=schema)

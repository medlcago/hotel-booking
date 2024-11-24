from dataclasses import dataclass

from core.exceptions import NotFoundException
from repositories.hotel import IHotelRepository
from schemas.hotel import HotelCreateRequest, HotelResponse, HotelCreateResponse, HotelParams
from schemas.pagination import PaginationResponse


@dataclass(frozen=True, slots=True)
class HotelService:
    hotel_repository: IHotelRepository

    async def add_hotel(self, schema: HotelCreateRequest) -> HotelCreateResponse:
        hotel = await self.hotel_repository.add_hotel(values=schema.model_dump())
        return HotelResponse.model_validate(hotel, from_attributes=True)

    async def get_hotel_by_id(self, hotel_id: int) -> HotelResponse:
        hotel = await self.hotel_repository.get_hotel_by_id(hotel_id)
        if not hotel:
            raise NotFoundException
        return HotelResponse.model_validate(hotel, from_attributes=True)

    async def get_hotels(self, params: HotelParams) -> PaginationResponse[HotelResponse]:
        result = await self.hotel_repository.get_hotels(**params.model_dump(exclude_none=True))
        return PaginationResponse[HotelResponse].model_validate(result, from_attributes=True)

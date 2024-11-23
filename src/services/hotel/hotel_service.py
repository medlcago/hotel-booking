from dataclasses import dataclass

from core.exceptions import NotFoundException
from core.uow import IUnitOfWork
from schemas.hotel import HotelCreateRequest, HotelResponse, HotelCreateResponse, HotelParams
from schemas.pagination import PaginationResponse


@dataclass(frozen=True, slots=True)
class HotelService:
    uow: IUnitOfWork

    async def add_hotel(self, schema: HotelCreateRequest) -> HotelCreateResponse:
        async with self.uow:
            hotel = await self.uow.hotel_repository.add_hotel(values=schema.model_dump())
            return HotelResponse.model_validate(hotel, from_attributes=True)

    async def get_hotel_by_id(self, hotel_id: int) -> HotelResponse:
        async with self.uow:
            hotel = await self.uow.hotel_repository.get_hotel_by_id(hotel_id)
            if not hotel:
                raise NotFoundException
            return HotelResponse.model_validate(hotel, from_attributes=True)

    async def get_hotels(self, params: HotelParams) -> PaginationResponse[HotelResponse]:
        async with self.uow:
            result = await self.uow.hotel_repository.get_hotels(**params.model_dump(exclude_none=True))
            return PaginationResponse[HotelResponse].model_validate(result, from_attributes=True)

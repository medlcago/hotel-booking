from dataclasses import dataclass

from core.exceptions import HotelNotFound
from core.uow import IUnitOfWork
from schemas.hotel import (
    HotelCreateRequest,
    HotelResponse,
    HotelCreateResponse,
    HotelParams,
    HotelUpdate
)
from schemas.response import PaginationResponse


@dataclass(frozen=True, slots=True)
class HotelService:
    uow: IUnitOfWork

    async def add_hotel(self, schema: HotelCreateRequest) -> HotelCreateResponse:
        async with self.uow as uow:
            hotel = await uow.hotel_repository.add_hotel(values=schema.model_dump())
            return HotelResponse.model_validate(hotel, from_attributes=True)

    async def get_hotel_by_id(self, hotel_id: int) -> HotelResponse:
        async with self.uow as uow:
            hotel = await uow.hotel_repository.get_hotel_by_id(hotel_id)
            if not hotel:
                raise HotelNotFound
            return HotelResponse.model_validate(hotel, from_attributes=True)

    async def get_hotels(self, params: HotelParams) -> PaginationResponse[HotelResponse]:
        async with self.uow as uow:
            result = await uow.hotel_repository.get_hotels(**params.model_dump(exclude_none=True))
            return PaginationResponse[HotelResponse].model_validate(result, from_attributes=True)

    async def update_hotel(self, hotel_id: int, schema: HotelUpdate) -> HotelUpdate:
        async with self.uow as uow:
            hotel = await uow.hotel_repository.update_hotel(
                hotel_id=hotel_id,
                values=schema.model_dump(exclude_unset=True)
            )
            if not hotel:
                raise HotelNotFound
            return HotelUpdate.model_validate(hotel, from_attributes=True)

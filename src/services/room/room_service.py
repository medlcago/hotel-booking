from dataclasses import dataclass

from core.exceptions import NotFoundException
from core.uow import IUnitOfWork
from schemas.pagination import PaginationResponse
from schemas.room import RoomCreateRequest, RoomResponse, RoomCreateResponse, RoomParams


@dataclass(frozen=True, slots=True)
class RoomService:
    uow: IUnitOfWork

    async def add_room(self, schema: RoomCreateRequest) -> RoomCreateResponse:
        async with self.uow:
            room = await self.uow.room_repository.add_room(values=schema.model_dump())
            return RoomCreateResponse.model_validate(room, from_attributes=True)

    async def get_room_by_id(self, room_id: int) -> RoomResponse:
        async with self.uow:
            room = await self.uow.room_repository.get_room_by_id(room_id=room_id)
            if not room:
                raise NotFoundException
            return RoomResponse.model_validate(room, from_attributes=True)

    async def get_rooms(self, params: RoomParams) -> PaginationResponse[RoomResponse]:
        async with self.uow:
            result = await self.uow.room_repository.get_rooms(**params.model_dump(exclude_none=True))
            return PaginationResponse[RoomResponse].model_validate(result, from_attributes=True)

from dataclasses import dataclass

from core.db.transactional import Transactional
from core.exceptions import RoomNotFound
from repositories.room_repo import IRoomRepository
from schemas.response import PaginationResponse
from schemas.room import (
    RoomCreateRequest,
    RoomResponse,
    RoomCreateResponse,
    RoomParams,
    RoomUpdate
)
from services.room_service import IRoomService

__all__ = ("RoomService",)


@dataclass(frozen=True, slots=True)
class RoomService(IRoomService):
    room_repository: IRoomRepository

    @Transactional()
    async def add_room(self, schema: RoomCreateRequest) -> RoomCreateResponse:
        room = await self.room_repository.add_room(values=schema.model_dump())
        return RoomCreateResponse.model_validate(room, from_attributes=True)

    async def get_room_by_id(self, room_id: int) -> RoomResponse:
        room = await self.room_repository.get_room_by_id(room_id=room_id)
        if not room:
            raise RoomNotFound
        return RoomResponse.model_validate(room, from_attributes=True)

    async def get_rooms(self, params: RoomParams) -> PaginationResponse[RoomResponse]:
        result = await self.room_repository.get_rooms(**params.model_dump(exclude_none=True))
        return PaginationResponse[RoomResponse].model_validate(result, from_attributes=True)

    @Transactional()
    async def update_room(self, room_id: int, schema: RoomUpdate) -> RoomUpdate:
        room = await self.room_repository.update_room(
            room_id=room_id,
            values=schema.model_dump(exclude_unset=True)
        )
        if not room:
            raise RoomNotFound
        return RoomUpdate.model_validate(room, from_attributes=True)

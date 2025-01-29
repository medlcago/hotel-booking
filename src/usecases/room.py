from dataclasses import dataclass

from core.db.transactional import Transactional
from domain.services import IRoomService
from domain.usecases import IRoomUseCase
from schemas.response import PaginationResponse
from schemas.room import RoomCreateRequest, RoomCreateResponse, RoomResponse, RoomParams, RoomUpdate

__all__ = ("RoomUseCase",)


@dataclass(frozen=True, slots=True)
class RoomUseCase(IRoomUseCase):
    room_service: IRoomService

    @Transactional()
    async def add_room(self, schema: RoomCreateRequest) -> RoomCreateResponse:
        return await self.room_service.add_room(schema=schema)

    async def get_room_by_id(self, room_id: int) -> RoomResponse:
        return await self.room_service.get_room_by_id(room_id=room_id)

    async def get_rooms(self, params: RoomParams) -> PaginationResponse[RoomResponse]:
        return await self.room_service.get_rooms(params=params)

    @Transactional()
    async def update_room(self, room_id: int, schema: RoomUpdate) -> RoomUpdate:
        return await self.room_service.update_room(room_id=room_id, schema=schema)

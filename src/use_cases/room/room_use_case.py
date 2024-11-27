from dataclasses import dataclass

from schemas.pagination import PaginationResponse
from schemas.room import (
    RoomCreateRequest,
    RoomResponse,
    RoomCreateResponse,
    RoomParams,
    RoomUpdate
)
from services.room import IRoomService


@dataclass(frozen=True, slots=True)
class RoomUseCase:
    room_service: IRoomService

    async def add_room(self, schema: RoomCreateRequest) -> RoomCreateResponse:
        room = await self.room_service.add_room(schema=schema)
        return room

    async def get_room_by_id(self, room_id: int) -> RoomResponse:
        room = await self.room_service.get_room_by_id(room_id=room_id)
        return room

    async def get_rooms(self, params: RoomParams) -> PaginationResponse[RoomResponse]:
        rooms = await self.room_service.get_rooms(params=params)
        return rooms

    async def update_room(self, room_id: int, schema: RoomUpdate) -> RoomUpdate:
        room = await self.room_service.update_room(room_id=room_id, schema=schema)
        return room

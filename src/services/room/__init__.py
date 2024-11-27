from typing import Protocol

from schemas.pagination import PaginationResponse
from schemas.room import (
    RoomCreateRequest,
    RoomResponse,
    RoomCreateResponse,
    RoomParams,
    RoomUpdate
)
from .room_service import RoomService


class IRoomService(Protocol):
    async def add_room(self, schema: RoomCreateRequest) -> RoomCreateResponse:
        ...

    async def get_room_by_id(self, room_id: int) -> RoomResponse:
        ...

    async def get_rooms(self, params: RoomParams) -> PaginationResponse[RoomResponse]:
        ...

    async def update_room(self, room_id: int, schema: RoomUpdate) -> RoomUpdate:
        ...

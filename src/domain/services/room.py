from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.response import PaginationResponse
    from schemas.room import (
        RoomCreateRequest,
        RoomResponse,
        RoomCreateResponse,
        RoomParams,
        RoomUpdate
    )


class IRoomService(ABC):
    @abstractmethod
    async def add_room(self, schema: RoomCreateRequest) -> RoomCreateResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_room_by_id(self, room_id: int) -> RoomResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_rooms(self, params: RoomParams) -> PaginationResponse[RoomResponse]:
        raise NotImplementedError

    @abstractmethod
    async def update_room(self, room_id: int, schema: RoomUpdate) -> RoomUpdate:
        raise NotImplementedError

from datetime import date
from typing import Protocol, Any

from models import Room
from repositories.base import Result
from .room_repo import RoomRepository


class IRoomRepository(Protocol):
    async def add_room(self, values: dict[str, Any]) -> Room:
        ...

    async def get_room_by_id(self, room_id: int) -> Room | None:
        ...

    async def get_rooms(
            self,
            limit: int,
            offset: int,
            date_from: date,
            date_to: date,
            **kwargs
    ) -> Result[Room]:
        ...

    async def update_room(self, room_id: int, values: dict[str, Any]) -> Room | None:
        ...

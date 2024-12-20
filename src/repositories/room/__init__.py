from abc import ABC
from datetime import date
from typing import Any

from models import Room
from repositories.base import Result


class IRoomRepository(ABC):
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

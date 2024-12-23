from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import date
    from models import Room
    from repositories.base import Result


class IRoomRepository(ABC):
    @abstractmethod
    async def add_room(self, values: dict[str, Any]) -> Room:
        raise NotImplementedError

    @abstractmethod
    async def get_room_by_id(self, room_id: int) -> Room | None:
        raise NotImplementedError

    @abstractmethod
    async def get_rooms(
            self,
            limit: int,
            offset: int,
            date_from: date,
            date_to: date,
            **kwargs
    ) -> Result[Room]:
        raise NotImplementedError

    @abstractmethod
    async def update_room(self, room_id: int, values: dict[str, Any]) -> Room | None:
        raise NotImplementedError

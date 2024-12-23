from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from models import User
    from repositories.base import Result


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, values: dict[str, Any]) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_users(self, limit: int, offset: int, **kwargs) -> Result[User]:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user_id: int, values: dict[str, Any]) -> User | None:
        raise NotImplementedError

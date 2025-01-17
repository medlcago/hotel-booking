from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities import User
    from schemas.response import PaginationResponse


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
    async def get_users(self, limit: int, offset: int, **kwargs) -> PaginationResponse[User]:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user_id: int, values: dict[str, Any]) -> User | None:
        raise NotImplementedError

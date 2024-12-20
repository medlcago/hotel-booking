from abc import ABC
from typing import Any

from models import User
from repositories.base import Result


class IUserRepository(ABC):
    async def create_user(self, values: dict[str, Any]) -> User:
        ...

    async def get_user_by_id(self, user_id: int) -> User | None:
        ...

    async def get_user_by_email(self, email: str) -> User | None:
        ...

    async def get_users(self, limit: int, offset: int, **kwargs) -> Result[User]:
        ...

    async def update_user(self, user_id: int, values: dict[str, Any]) -> User | None:
        ...

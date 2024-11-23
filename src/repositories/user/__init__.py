from typing import Protocol, Any

from models import User
from .user_repo import UserRepository


class IUserRepository(Protocol):
    async def create_user(self, values: dict[str, Any]) -> User:
        ...

    async def get_user_by_id(self, user_id: int) -> User | None:
        ...

    async def get_user_by_email(self, email: str) -> User | None:
        ...

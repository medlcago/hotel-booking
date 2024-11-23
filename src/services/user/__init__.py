from typing import Protocol

from schemas.user import UserResponse
from .user_service import UserService


class IUserService(Protocol):
    async def get_user_by_email(self, email: str) -> UserResponse:
        ...

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        ...

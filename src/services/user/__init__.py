from typing import Protocol

from schemas.pagination import PaginationResponse
from schemas.user import UserResponse, UserParams
from .user_service import UserService


class IUserService(Protocol):
    async def get_user_by_email(self, email: str) -> UserResponse:
        ...

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        ...

    async def get_users(self, params: UserParams) -> PaginationResponse[UserResponse]:
        ...

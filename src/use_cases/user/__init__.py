from typing import Protocol

from schemas.pagination import PaginationResponse
from schemas.user import UserResponse, UserParams
from .user_use_case import UserUseCase


class IUserUseCase(Protocol):
    async def get_users(self, params: UserParams) -> PaginationResponse[UserResponse]:
        ...

from typing import Protocol

from schemas.response import Message
from schemas.response import PaginationResponse
from schemas.user import (
    UserResponse,
    UserParams,
    PasswordResetRequest,
    PasswordResetConfirm
)
from .user_use_case import UserUseCase


class IUserUseCase(Protocol):
    async def get_users(self, params: UserParams) -> PaginationResponse[UserResponse]:
        ...

    async def reset_password(self, schema: PasswordResetRequest) -> Message:
        ...

    async def confirm_reset_password(self, schema: PasswordResetConfirm) -> Message:
        ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.response import Message
    from schemas.response import PaginationResponse
    from schemas.user import (
        UserResponse,
        UserParams,
        PasswordResetRequest,
        PasswordResetConfirm,
    )


class IUserService(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_users(self, params: UserParams) -> PaginationResponse[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    async def reset_password(self, schema: PasswordResetRequest) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def confirm_reset_password(self, schema: PasswordResetConfirm) -> Message:
        raise NotImplementedError

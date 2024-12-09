from dataclasses import dataclass

from schemas.response import Message
from schemas.response import PaginationResponse
from schemas.user import (
    UserParams,
    UserResponse,
    PasswordResetRequest,
    PasswordResetConfirm
)
from services.user import IUserService


@dataclass(frozen=True, slots=True)
class UserUseCase:
    user_service: IUserService

    async def get_users(self, params: UserParams) -> PaginationResponse[UserResponse]:
        return await self.user_service.get_users(params=params)

    async def reset_password(self, schema: PasswordResetRequest) -> Message:
        return await self.user_service.reset_password(schema=schema)

    async def confirm_reset_password(self, schema: PasswordResetConfirm) -> Message:
        return await self.user_service.confirm_reset_password(schema=schema)

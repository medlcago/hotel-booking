from dataclasses import dataclass

from core.db.transactional import Transactional
from domain.services import IUserService
from domain.usecases import IUserUseCase
from schemas.response import PaginationResponse, Message
from schemas.user import (
    UserResponse,
    UserParams,
    PasswordResetRequest,
    PasswordResetConfirm
)

__all__ = ("UserUseCase",)


@dataclass(frozen=True, slots=True)
class UserUseCase(IUserUseCase):
    user_service: IUserService

    async def get_user_by_email(self, email: str) -> UserResponse:
        return await self.user_service.get_user_by_email(email=email)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        return await self.user_service.get_user_by_id(user_id=user_id)

    async def get_users(self, params: UserParams) -> PaginationResponse[UserResponse]:
        return await self.user_service.get_users(params=params)

    async def reset_password(self, schema: PasswordResetRequest) -> Message:
        return await self.user_service.reset_password(schema=schema)

    @Transactional()
    async def confirm_reset_password(self, schema: PasswordResetConfirm) -> Message:
        return await self.user_service.confirm_reset_password(schema=schema)

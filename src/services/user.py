from dataclasses import dataclass
from datetime import timedelta

from celery import Celery

from core import security
from core.exceptions import (
    UserNotFound,
    InvalidCode,
    CodeAlreadySent
)
from domain.repositories import IUserRepository
from domain.services import IUserService
from schemas.response import Message
from schemas.response import PaginationResponse
from schemas.user import (
    UserResponse,
    UserParams,
    PasswordResetRequest,
    PasswordResetConfirm
)
from stores.base import Store

__all__ = ("UserService",)


@dataclass(frozen=True, slots=True)
class UserService(IUserService):
    user_repository: IUserRepository
    celery: Celery
    store: Store

    async def get_user_by_email(self, email: str) -> UserResponse:
        user = await self.user_repository.get_user_by_email(email=email)
        if not user:
            raise UserNotFound
        return UserResponse.model_validate(user, from_attributes=True)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFound
        return UserResponse.model_validate(user, from_attributes=True)

    async def get_users(self, params: UserParams) -> PaginationResponse[UserResponse]:
        users = await self.user_repository.get_users(**params.model_dump(exclude_none=True))
        return PaginationResponse[UserResponse].model_validate(
            users,
            from_attributes=True
        )

    async def reset_password(self, schema: PasswordResetRequest) -> Message:
        user = await self.user_repository.get_user_by_email(email=str(schema.email))
        if not user:
            raise UserNotFound
        key = f"reset_password:{schema.email}"
        expires_in = await self.store.expires_in(key)
        if expires_in:
            raise CodeAlreadySent(headers={
                "Retry-After": str(expires_in)
            })
        code = security.generate_code()
        self.celery.send_task(name="send_reset_password_code", args=(schema.email, code))
        await self.store.set(key, code, timedelta(minutes=2))
        return Message(
            message="A password reset code has been sent to your email address!",
        )

    async def confirm_reset_password(self, schema: PasswordResetConfirm) -> Message:
        key = f"reset_password:{schema.email}"
        code = await self.store.get(key)
        if not code or code.decode("utf-8") != schema.code:
            raise InvalidCode
        user = await self.user_repository.get_user_by_email(email=schema.email)
        if not user:
            raise InvalidCode
        hashed_password = security.hash_password(schema.new_password)
        await self.user_repository.update_user(user_id=user.id, values=dict(password=hashed_password))
        await self.store.delete(key)
        return Message(
            message="Password reset successful!",
        )

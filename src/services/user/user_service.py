from dataclasses import dataclass

from core import security
from core.exceptions import (
    TokenExpired,
    UserNotFound
)
from repositories.user import IUserRepository
from schemas.response import Message
from schemas.response import PaginationResponse
from schemas.user import (
    UserResponse,
    UserParams,
    PasswordResetRequest,
    PasswordResetConfirm
)
from tasks import send_reset_password_email


@dataclass(frozen=True, slots=True)
class UserService:
    user_repository: IUserRepository

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
        user = await self.user_repository.get_user_by_email(email=schema.email)
        if not user:
            raise UserNotFound
        token = security.create_url_safe_token(data=dict(email=schema.email, action="reset_password"))
        send_reset_password_email.delay(email=schema.email, token=token)
        return Message(
            message="An email has been sent to your email address to reset your password!",
        )

    async def confirm_reset_password(self, schema: PasswordResetConfirm) -> Message:
        payload = security.decode_url_safe_token(token=schema.token, max_age=300)
        if not payload:
            raise TokenExpired
        email, action = payload.get("email"), payload.get("action")
        if not email or action != "reset_password":
            raise TokenExpired
        user = await self.user_repository.get_user_by_email(email=email)
        if not user:
            raise TokenExpired
        hashed_password = security.hash_password(schema.new_password)
        await self.user_repository.update_user(user_id=user.id, values=dict(password=hashed_password))
        return Message(
            message="Password reset successful!",
        )

from dataclasses import dataclass

from schemas.auth import SignInRequest
from schemas.auth import SignUpRequest
from schemas.response import Message
from schemas.token import Token
from schemas.user import UserResponse
from services.auth import IAuthService


@dataclass(frozen=True, slots=True)
class AuthUseCase:
    auth_service: IAuthService

    async def register_user(self, schema: SignUpRequest) -> UserResponse:
        return await self.auth_service.sign_up(schema=schema)

    async def login_user(self, schema: SignInRequest) -> Token:
        return await self.auth_service.sign_in(schema=schema)

    async def refresh_token(self, user_id: int) -> Token:
        return await self.auth_service.refresh_token(user_id=user_id)

    async def confirm_email(self, token: str) -> Message:
        return await self.auth_service.confirm_email(token=token)

    async def send_confirmation_email(self, email: str) -> Message:
        return await self.auth_service.send_confirmation_email(email=email)

from dataclasses import dataclass

from schemas.auth import SignInRequest
from schemas.auth import SignUpRequest
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

    async def verify_email(self, token: str) -> None:
        return await self.auth_service.verify_email(token=token)

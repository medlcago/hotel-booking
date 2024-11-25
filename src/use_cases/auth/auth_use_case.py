from dataclasses import dataclass

from schemas.auth import SignInRequest
from schemas.auth import SignUpRequest
from schemas.token import Token, RefreshToken
from services.auth import IAuthService


@dataclass(frozen=True, slots=True)
class AuthUseCase:
    auth_service: IAuthService

    async def register(self, schema: SignUpRequest) -> Token:
        token = await self.auth_service.sign_up(schema=schema)
        return token

    async def login(self, schema: SignInRequest) -> Token:
        token = await self.auth_service.sign_in(schema=schema)
        return token

    async def refresh_token(self, schema: RefreshToken) -> Token:
        return await self.auth_service.refresh_token(schema=schema)

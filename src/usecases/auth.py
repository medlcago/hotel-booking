from dataclasses import dataclass

from core.db.transactional import Transactional
from domain.services import IAuthService
from domain.usecases import IAuthUseCase
from schemas.auth import SignUpRequest, SignInRequest, ConfirmEmailRequest
from schemas.response import Message
from schemas.token import TokenResult, Token

__all__ = ("AuthUseCase",)


@dataclass(frozen=True, slots=True)
class AuthUseCase(IAuthUseCase):
    auth_service: IAuthService

    @Transactional()
    async def sign_up(self, schema: SignUpRequest) -> Token:
        return await self.auth_service.sign_up(schema=schema)

    async def sign_in(self, schema: SignInRequest) -> Token:
        return await self.auth_service.sign_in(schema=schema)

    async def refresh_token(self, token: TokenResult) -> Token:
        return await self.auth_service.refresh_token(token=token)

    @Transactional()
    async def confirm_email(self, schema: ConfirmEmailRequest) -> Message:
        return await self.auth_service.confirm_email(schema=schema)

    async def send_confirmation_code(self, email: str) -> Message:
        return await self.auth_service.send_confirmation_code(email=email)

    async def revoke_token(self, token: TokenResult) -> None:
        return await self.auth_service.revoke_token(token=token)

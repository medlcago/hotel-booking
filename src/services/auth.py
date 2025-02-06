from dataclasses import dataclass
from datetime import timedelta

from celery import Celery

from core import security
from core.exceptions import (
    UserAlreadyExists,
    BadCredentials,
    UserInactive,
    TokenExpired,
    UserAlreadyVerified,
    InvalidCode,
    CodeAlreadySent,
)
from core.settings import settings
from domain.repositories import IUserRepository
from domain.services import IAuthService
from enums.token import TokenType
from schemas.auth import SignInRequest, ConfirmEmailRequest
from schemas.auth import SignUpRequest
from schemas.response import Message
from schemas.token import Token, TokenResult
from stores.base import Store

__all__ = ("AuthService",)


@dataclass(frozen=True, slots=True)
class AuthService(IAuthService):
    user_repository: IUserRepository
    store: Store
    celery: Celery

    async def sign_up(self, schema: SignUpRequest) -> Token:
        user = await self.user_repository.get_user_by_email(email=str(schema.email))
        if user:
            raise UserAlreadyExists

        schema.password = security.hash_password(schema.password)
        user = await self.user_repository.create_user(values=schema.model_dump())
        key = f"confirmation_code:{schema.email}"
        code = security.generate_code()
        await self.store.set(key, code, timedelta(minutes=2))
        self._send_code(email=user.email, code=code)
        return self.get_token(user_id=user.id)

    async def sign_in(self, schema: SignInRequest) -> Token:
        user = await self.user_repository.get_user_by_email(email=str(schema.email))
        if not user:
            raise BadCredentials
        if not security.verify_password(password=schema.password, hashed_password=user.password):
            raise BadCredentials
        if not user.is_active:
            raise UserInactive
        return self.get_token(user_id=user.id)

    @staticmethod
    def get_token(user_id: int) -> Token:
        access_token = security.create_access_token(identity=user_id)
        refresh_token = security.create_refresh_token(identity=user_id)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def refresh_token(self, token: TokenResult) -> Token:
        await self.revoke_token(token=token)
        return self.get_token(user_id=token.user_id)

    async def confirm_email(self, schema: ConfirmEmailRequest) -> Message:
        key = f"confirmation_code:{schema.email}"
        code = await self.store.get(key)
        if not code or code.decode("utf-8") != schema.code:
            raise InvalidCode
        user = await self.user_repository.get_user_by_email(email=schema.email)
        if not user or user.is_verified:
            raise InvalidCode
        await self.user_repository.update_user(user_id=user.id, values=dict(is_verified=True))
        await self.store.delete(key)
        return Message(
            message="E-mail successfully confirmed!"
        )

    async def send_confirmation_code(self, email: str) -> Message:
        user = await self.user_repository.get_user_by_email(email=email)
        if not user:
            raise BadCredentials
        if user.is_verified:
            raise UserAlreadyVerified
        key = f"confirmation_code:{email}"
        expires_in = await self.store.expires_in(key)
        if expires_in:
            raise CodeAlreadySent(headers={
                "Retry-After": str(expires_in)
            })
        code = security.generate_code()
        await self.store.set(key, code, timedelta(minutes=2))
        self._send_code(email=email, code=code)
        return Message(
            message="E-mail successfully sent!"
        )

    def _send_code(self, email: str, code: str) -> None:
        self.celery.send_task(name="send_confirmation_code", args=(email, code))

    async def revoke_token(self, token: TokenResult) -> None:
        key = f"{token.token_type}:{token.token}:{token.user_id}"
        exists = await self.store.exists(key=key)
        if exists:
            raise TokenExpired

        is_refresh_token = token.token_type == TokenType.refresh
        expires_in = settings.refresh_token_lifetime if is_refresh_token else settings.access_token_lifetime
        await self.store.set(key=key, value=token.token, expires_in=expires_in)

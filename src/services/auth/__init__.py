from typing import Protocol

from schemas.auth import (
    SignInRequest,
    SignUpRequest
)
from schemas.response import Message
from schemas.token import Token, TokenResult
from schemas.user import UserResponse
from .auth_service import AuthService


class IAuthService(Protocol):
    async def sign_up(self, schema: SignUpRequest) -> UserResponse:
        ...

    async def sign_in(self, schema: SignInRequest) -> Token:
        ...

    @staticmethod
    def get_token(user_id: int) -> Token:
        ...

    async def refresh_token(self, result: TokenResult) -> Token:
        ...

    async def confirm_email(self, token: str) -> Message:
        ...

    async def send_confirmation_email(self, email: str) -> Message:
        ...

    async def revoke_token(self, result: TokenResult) -> None:
        ...

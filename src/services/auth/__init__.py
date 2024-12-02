from typing import Protocol

from schemas.auth import (
    SignInRequest,
    SignUpRequest
)
from schemas.token import Token
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

    async def refresh_token(self, user_id: int) -> Token:
        ...

    async def verify_email(self, token: str) -> None:
        ...

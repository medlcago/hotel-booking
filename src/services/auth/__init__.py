from typing import Protocol

from schemas.auth import (
    SignInRequest,
    SignUpRequest
)
from schemas.token import (
    Token,
    RefreshToken
)
from .auth_service import AuthService


class IAuthService(Protocol):
    async def sign_up(self, schema: SignUpRequest) -> Token:
        ...

    async def sign_in(self, schema: SignInRequest) -> Token:
        ...

    @staticmethod
    def get_token(user_id: int) -> Token:
        ...

    async def refresh_token(self, token: RefreshToken) -> Token:
        ...

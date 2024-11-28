from typing import Protocol

from schemas.auth import SignInRequest
from schemas.auth import SignUpRequest
from schemas.token import Token
from .auth_use_case import AuthUseCase


class IAuthUseCase(Protocol):
    async def register(self, schema: SignUpRequest) -> Token:
        ...

    async def login(self, schema: SignInRequest) -> Token:
        ...

    async def refresh_token(self, user_id: int) -> Token:
        ...

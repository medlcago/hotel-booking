from typing import Protocol

from schemas.auth import SignInRequest
from schemas.auth import SignUpRequest
from schemas.response import Message
from schemas.token import Token
from schemas.user import UserResponse
from .auth_use_case import AuthUseCase


class IAuthUseCase(Protocol):
    async def register_user(self, schema: SignUpRequest) -> UserResponse:
        ...

    async def login_user(self, schema: SignInRequest) -> Token:
        ...

    async def refresh_token(self, user_id: int) -> Token:
        ...

    async def confirm_email(self, token: str) -> Message:
        ...

    async def send_confirmation_email(self, email: str) -> Message:
        ...

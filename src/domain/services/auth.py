from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.auth import (
        SignInRequest,
        SignUpRequest
    )
    from schemas.response import Message
    from schemas.token import Token, TokenResult
    from schemas.user import UserResponse


class IAuthService(ABC):
    @abstractmethod
    async def sign_up(self, schema: SignUpRequest) -> UserResponse:
        raise NotImplementedError

    @abstractmethod
    async def sign_in(self, schema: SignInRequest) -> Token:
        raise NotImplementedError

    @abstractmethod
    async def refresh_token(self, token: TokenResult) -> Token:
        raise NotImplementedError

    @abstractmethod
    async def confirm_email(self, token: str) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def send_confirmation_email(self, email: str) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def revoke_token(self, token: TokenResult) -> None:
        raise NotImplementedError

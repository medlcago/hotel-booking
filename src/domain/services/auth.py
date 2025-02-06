from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.auth import (
        SignInRequest,
        SignUpRequest,
        ConfirmEmailRequest
    )
    from schemas.response import Message
    from schemas.token import Token, TokenResult


class IAuthService(ABC):
    @abstractmethod
    async def sign_up(self, schema: SignUpRequest) -> Token:
        raise NotImplementedError

    @abstractmethod
    async def sign_in(self, schema: SignInRequest) -> Token:
        raise NotImplementedError

    @abstractmethod
    async def refresh_token(self, token: TokenResult) -> Token:
        raise NotImplementedError

    @abstractmethod
    async def confirm_email(self, schema: ConfirmEmailRequest) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def send_confirmation_code(self, email: str) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def revoke_token(self, token: TokenResult) -> None:
        raise NotImplementedError

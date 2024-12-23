from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from email.message import EmailMessage, Message
    from typing import Literal

    from aiosmtplib import SMTPResponse


class IEmailService(ABC):
    @abstractmethod
    async def send_email(
            self,
            subject: str,
            recipients: list[str],
            body: str,
            content_type: Literal["html", "plain"],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def send(
            self,
            msg: EmailMessage | Message,
            *,
            recipients: list[str] | None = None
    ) -> tuple[dict[str, SMTPResponse], str]:
        raise NotImplementedError

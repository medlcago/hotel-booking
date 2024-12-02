from email.message import EmailMessage, Message
from typing import Protocol, Literal

from aiosmtplib import SMTPResponse

from .email_service import EmailService


class IEmailService(Protocol):
    async def send_email(
            self,
            subject: str,
            recipients: list[str],
            body: str,
            content_type: Literal["html", "plain"],
    ) -> None:
        ...

    async def send(
            self,
            msg: EmailMessage | Message,
            recipients: list[str] | None = None
    ) -> tuple[dict[str, SMTPResponse], str]:
        ...

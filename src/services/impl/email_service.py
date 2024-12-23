import logging
from dataclasses import dataclass
from email.message import EmailMessage, Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Literal

import aiosmtplib
from aiosmtplib import SMTPResponse

from services.email_service import IEmailService

__all__ = ("EmailService",)

logger = logging.getLogger("hotel_booking")


@dataclass(frozen=True, slots=True)
class EmailService(IEmailService):
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    async def send_email(
            self,
            subject: str,
            recipients: list[str],
            body: str,
            content_type: Literal["html", "plain"],
    ) -> None:
        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html" if content_type == "html" else "plain", "utf-8"))
        await self.send(
            msg=msg,
            recipients=recipients,
        )

    async def send(
            self,
            msg: EmailMessage | Message,
            *,
            recipients: list[str] | None = None
    ) -> tuple[dict[str, SMTPResponse], str]:
        try:
            async with aiosmtplib.SMTP(
                    hostname=self.smtp_server,
                    port=self.smtp_port,
                    username=self.smtp_user,
                    password=self.smtp_password,
            ) as server:
                response = await server.send_message(
                    msg,
                    recipients=recipients,
                )
                logger.info(f"Email sent to {recipients}")
                return response
        except Exception as ex:
            logger.exception(f"Error sending email: {ex}")

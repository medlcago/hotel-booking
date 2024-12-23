from typing import Literal

from core.settings import settings
from services.impl.email_service import EmailService


async def send_email(
        subject: str,
        recipients: list[str],
        body: str,
        content_type: Literal["html", "plain"]
) -> None:
    email_service = EmailService(
        smtp_server=settings.smtp_server.host,
        smtp_port=settings.smtp_server.port,
        smtp_user=settings.smtp_server.username,
        smtp_password=settings.smtp_server.password,
    )
    await email_service.send_email(
        subject=subject,
        recipients=recipients,
        body=body,
        content_type=content_type,
    )

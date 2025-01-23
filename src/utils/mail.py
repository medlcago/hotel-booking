from typing import Literal

from dependency_injector.wiring import Provide, inject

from core.container import Container
from domain.services import IEmailService


@inject
async def send_email(
        subject: str,
        recipients: list[str],
        body: str,
        content_type: Literal["html", "plain"],
        email_service: IEmailService = Provide[Container.email_service]
) -> None:
    await email_service.send_email(
        subject=subject,
        recipients=recipients,
        body=body,
        content_type=content_type,
    )

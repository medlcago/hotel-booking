from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal


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

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from schemas.payment import (
        PaymentCreateResponse,
        PaymentResponse
    )
    from schemas.response import PaginationResponse


class IPaymentService(ABC):
    @abstractmethod
    async def create_payment(self, params: dict[str, Any]) -> PaymentCreateResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_user_payment(self, booking_id: int, user_id: int) -> PaymentResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_user_payments(self, user_id: int) -> PaginationResponse[PaymentResponse]:
        raise NotImplementedError

    @abstractmethod
    async def capture_payment(self, booking_id: int, user_id: int) -> None:
        raise NotImplementedError

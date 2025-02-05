from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from enums.payment import PaymentMethod

if TYPE_CHECKING:
    from domain.entities import Payment
    from schemas.response import PaginationResponse


class IPaymentRepository(ABC):
    @abstractmethod
    async def create_payment(self, values: dict[str, Any]) -> Payment:
        raise NotImplementedError

    @abstractmethod
    async def get_payment(self, booking_id: int, user_id: int, payment_method: PaymentMethod) -> Payment | None:
        raise NotImplementedError

    @abstractmethod
    async def get_payments(self, user_id: int, payment_method: PaymentMethod) -> PaginationResponse[Payment]:
        raise NotImplementedError

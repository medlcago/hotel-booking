from abc import ABC, abstractmethod
from typing import Mapping, Any

from enums.currency import Currency


class IPaymentService(ABC):
    @abstractmethod
    async def create_payment(self, amount: float, currency: Currency, payment_details: Mapping[str, Any]):
        raise NotImplementedError

    @abstractmethod
    async def get_payment(self, payment_id: str):
        raise NotImplementedError

    @abstractmethod
    async def cancel_payment(self, payment_id: str):
        raise NotImplementedError

    @abstractmethod
    async def capture_payment(self, payment_id: str, amount: float | None = None):
        raise NotImplementedError

    @abstractmethod
    async def refund_payment(self, payment_id: str, amount: float):
        raise NotImplementedError

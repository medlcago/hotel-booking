import uuid
from dataclasses import dataclass
from typing import Any, cast

from asgiref.sync import sync_to_async
from yookassa import Configuration, Payment

from core.exceptions import PaymentNotFound
from domain.repositories import IPaymentRepository
from domain.services.payment import IPaymentService
from enums.currency import Currency
from enums.payment import PaymentMethod
from schemas.payment import (
    PaymentCreateResponse,
    PaymentResponse
)
from schemas.response import PaginationResponse

__all__ = ("YookassaService",)


@dataclass(frozen=True, slots=True)
class YookassaService(IPaymentService):
    shop_id: str
    secret_key: str
    payment_repository: IPaymentRepository

    def __post_init__(self):
        Configuration.configure(self.shop_id, self.secret_key)

    async def create_payment(self, params: dict[str, Any]) -> PaymentCreateResponse:
        yookassa_payment = await sync_to_async(Payment.create)(
            params=params,
            idempotency_key=uuid.uuid4()
        )

        metadata = cast(dict, params.get("metadata"))
        booking_id = cast(int, metadata.get("booking_id"))
        user_id = cast(int, metadata.get("user_id"))

        payment = await self.payment_repository.create_payment(
            values=dict(
                payment_id=yookassa_payment.id,
                payment_method=PaymentMethod.yookassa,
                amount=yookassa_payment.amount.value,
                currency=yookassa_payment.amount.currency,
                booking_id=booking_id,
                user_id=user_id,
            )
        )
        return PaymentCreateResponse(
            id=payment.id,
            payment_id=payment.payment_id,
            payment_method=PaymentMethod(payment.payment_method),
            amount=payment.amount,
            currency=Currency(payment.currency),
            payment_url=yookassa_payment.confirmation.confirmation_url,
            booking_id=payment.booking_id,
            user_id=payment.user_id,
            created_at=payment.created_at
        )

    async def get_user_payment(self, booking_id: int, user_id: int) -> PaymentResponse:
        payment = await self.payment_repository.get_payment(
            booking_id=booking_id,
            user_id=user_id,
            payment_method=PaymentMethod.yookassa
        )
        if not payment:
            raise PaymentNotFound
        return PaymentResponse.model_validate(payment, from_attributes=True)

    async def get_user_payments(self, user_id: int) -> PaginationResponse[PaymentResponse]:
        result = await self.payment_repository.get_payments(
            user_id=user_id,
            payment_method=PaymentMethod.yookassa
        )
        return PaginationResponse[PaymentResponse].model_validate(
            result,
            from_attributes=True
        )

    async def capture_payment(self, booking_id: int, user_id: int) -> None:
        payment = await self.get_user_payment(
            booking_id=booking_id,
            user_id=user_id
        )
        await sync_to_async(Payment.capture)(
            payment_id=payment.payment_id,
            idempotency_key=uuid.uuid4(),
            params=None
        )

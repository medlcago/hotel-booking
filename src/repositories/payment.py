from typing import Any

from sqlalchemy import insert, select, func

from domain.entities import Payment
from domain.repositories import IPaymentRepository
from domain.repositories.base import Repository
from enums.payment import PaymentMethod
from schemas.response import PaginationResponse

__all__ = ("PaymentRepository",)


class PaymentRepository(IPaymentRepository, Repository[Payment]):
    table = Payment

    async def create_payment(self, values: dict[str, Any]) -> Payment:
        payment_stmt = (
            insert(self.table).
            values(**values).
            returning(self.table)
        )
        return await self.session.scalar(payment_stmt)

    async def get_payment(self, booking_id: int, user_id: int, payment_method: PaymentMethod) -> Payment | None:
        payment_stmt = (
            select(self.table).
            filter_by(
                booking_id=booking_id,
                user_id=user_id,
                payment_method=payment_method
            )
        )
        return await self.session.scalar(payment_stmt)

    async def get_payments(self, user_id: int, payment_method: PaymentMethod) -> PaginationResponse[Payment]:
        payments_stmt = (
            select(self.table).
            filter_by(
                user_id=user_id,
                payment_method=payment_method
            )
        )
        count_stmt = (
            select(func.count(self.table.id)).
            filter_by(
                user_id=user_id,
                payment_method=payment_method
            )
        )
        payments = (await self.session.scalars(payments_stmt)).all()
        count = await self.session.scalar(count_stmt)
        return PaginationResponse(
            count=count,
            items=payments
        )

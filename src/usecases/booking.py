from dataclasses import dataclass

from core.db.transactional import Transactional
from core.settings import settings
from domain.services import IBookingService, IPaymentService
from domain.usecases import IBookingUseCase
from enums.currency import Currency
from schemas.booking import (
    BookingCreateRequest,
    BookingCancelRequest,
    BookingParams,
    BookingResponse,
    BookingPaymentResponse
)
from schemas.response import PaginationResponse

__all__ = ("BookingUseCase",)


@dataclass(frozen=True, slots=True)
class BookingUseCase(IBookingUseCase):
    booking_service: IBookingService
    payment_service: IPaymentService

    @Transactional()
    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingPaymentResponse:
        booking = await self.booking_service.create_booking(
            schema=schema,
            user_id=user_id
        )
        payment = await self.payment_service.create_payment(
            params=dict(
                amount=dict(
                    value=booking.total_cost,
                    currency=Currency.RUB
                ),
                metadata=dict(
                    booking_id=booking.id,
                    user_id=user_id
                ),
                confirmation=dict(
                    type="redirect",
                    return_url=settings.yookassa.return_url
                ),
                capture=False
            )
        )
        return BookingPaymentResponse(
            **booking.model_dump(),
            payment=payment
        )

    @Transactional()
    async def cancel_booking(self, schema: BookingCancelRequest, user_id: int) -> None:
        await self.booking_service.cancel_booking(
            booking_id=schema.booking_id,
            user_id=user_id
        )

    @Transactional()
    async def confirm_booking(self, booking_id: int, user_id: int) -> None:
        await self.booking_service.confirm_booking(
            booking_id=booking_id,
            user_id=user_id,
        )
        await self.payment_service.capture_payment(
            booking_id=booking_id,
            user_id=user_id,
        )

    async def get_user_bookings(self, user_id: int, params: BookingParams) -> PaginationResponse[BookingResponse]:
        return await self.booking_service.get_user_bookings(
            user_id=user_id,
            params=params
        )

    async def get_user_booking(self, booking_id: int, user_id: int) -> BookingResponse:
        return await self.booking_service.get_user_booking(
            booking_id=booking_id,
            user_id=user_id
        )

    @Transactional()
    async def cancel_pending_booking(self, booking_id: int, user_id: int) -> None:
        await self.booking_service.cancel_pending_booking(booking_id=booking_id, user_id=user_id)

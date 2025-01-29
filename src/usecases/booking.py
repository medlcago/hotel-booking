from dataclasses import dataclass

from core.db.transactional import Transactional
from domain.services import IBookingService
from domain.usecases import IBookingUseCase
from schemas.booking import (
    BookingCreateRequest,
    BookingCancelRequest,
    BookingParams,
    BookingResponse,
    BookingCreateResponse
)
from schemas.response import PaginationResponse

__all__ = ("BookingUseCase",)


@dataclass(frozen=True, slots=True)
class BookingUseCase(IBookingUseCase):
    booking_service: IBookingService

    @Transactional()
    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingCreateResponse:
        return await self.booking_service.create_booking(
            schema=schema,
            user_id=user_id
        )

    @Transactional()
    async def cancel_booking(self, schema: BookingCancelRequest, user_id: int) -> None:
        await self.booking_service.cancel_booking(
            booking_id=schema.booking_id,
            user_id=user_id
        )

    @Transactional()
    async def confirm_booking(self, booking_id: int) -> None:
        await self.booking_service.confirm_booking(
            booking_id=booking_id,
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

    async def get_booking(self, booking_id: int) -> BookingResponse:
        return await self.booking_service.get_booking(booking_id=booking_id)

    async def cancel_pending_booking(self, booking_id: int) -> None:
        return await self.booking_service.cancel_pending_booking(booking_id=booking_id)

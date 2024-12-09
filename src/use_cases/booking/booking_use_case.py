from dataclasses import dataclass

from schemas.booking import (
    BookingCreateRequest,
    BookingResponse,
    BookingCreateResponse,
    BookingParams,
    BookingCancelRequest
)
from schemas.response import PaginationResponse
from services.booking import IBookingService


@dataclass(frozen=True, slots=True)
class BookingUseCase:
    booking_service: IBookingService

    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingCreateResponse:
        return await self.booking_service.create_booking(schema=schema, user_id=user_id)

    async def cancel_booking(self, schema: BookingCancelRequest, user_id: int) -> None:
        return await self.booking_service.cancel_booking(schema=schema, user_id=user_id)

    async def get_bookings(self, user_id: int, params: BookingParams) -> PaginationResponse[BookingResponse]:
        return await self.booking_service.get_bookings(user_id=user_id, params=params)

    async def get_booking(self, booking_id: int, user_id: int) -> BookingResponse:
        return await self.booking_service.get_booking(booking_id=booking_id, user_id=user_id)

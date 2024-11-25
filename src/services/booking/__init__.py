from typing import Protocol

from schemas.booking import BookingCreateRequest, BookingResponse, BookingCreateResponse, BookingParams
from schemas.pagination import PaginationResponse
from .booking_service import BookingService


class IBookingService(Protocol):
    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingCreateResponse:
        ...

    async def cancel_booking(self, booking_id: int, user_id: int) -> None:
        ...

    async def get_bookings(self, user_id: int, params: BookingParams) -> PaginationResponse[BookingResponse]:
        ...

    async def get_booking(self, booking_id: int, user_id: int) -> BookingResponse:
        ...

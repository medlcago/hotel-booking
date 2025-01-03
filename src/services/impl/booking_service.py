from dataclasses import dataclass
from datetime import date

from core.db.transactional import Transactional
from core.exceptions import (
    RoomNotFound,
    RoomAlreadyBooked,
    BookingNotFound,
    BookingCancelNotAllowed,
    BookingConfirmNotAllowed
)
from enums.status import BookingStatus
from repositories.booking_repo import IBookingRepository
from repositories.room_repo import IRoomRepository
from schemas.booking import (
    BookingCreateRequest,
    BookingResponse,
    BookingCreateResponse,
    BookingParams,
    BookingCancelRequest
)
from schemas.response import PaginationResponse
from services.booking_service import IBookingService

__all__ = ("BookingService",)


@dataclass(frozen=True, slots=True)
class BookingService(IBookingService):
    room_repository: IRoomRepository
    booking_repository: IBookingRepository

    @Transactional()
    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingCreateResponse:
        room = await self.room_repository.get_room_by_id(room_id=schema.room_id)
        if not room:
            raise RoomNotFound
        room_booking = await self.booking_repository.get_room_booking(
            room_id=schema.room_id,
            date_from=schema.date_from,
            date_to=schema.date_to,
        )
        if room_booking:
            raise RoomAlreadyBooked

        booking = await self.booking_repository.create_booking(
            values=dict(**schema.model_dump(), user_id=user_id)
        )
        return BookingCreateResponse.model_validate(booking, from_attributes=True)

    @Transactional()
    async def cancel_booking(self, schema: BookingCancelRequest, user_id: int) -> None:
        booking = await self.booking_repository.get_user_booking(booking_id=schema.booking_id, user_id=user_id)
        if not booking:
            raise BookingNotFound
        if booking.status != BookingStatus.pending or booking.date_to <= date.today():
            raise BookingCancelNotAllowed
        await self.booking_repository.update_booking(
            booking_id=schema.booking_id,
            values=dict(status=BookingStatus.canceled)
        )

    @Transactional()
    async def confirm_booking(self, booking_id: int, payment_id: str) -> None:
        # TODO: add payment service
        booking = await self.booking_repository.get_booking(booking_id=booking_id)
        if not booking:
            raise BookingNotFound
        if booking.status != BookingStatus.pending:
            raise BookingConfirmNotAllowed(
                f"Confirmation of booking is not allowed. Current status: {booking.status}"
            )
        await self.booking_repository.update_booking(
            booking_id=booking_id,
            values=dict(status=BookingStatus.confirmed)
        )

    async def get_user_bookings(self, user_id: int, params: BookingParams) -> PaginationResponse[BookingResponse]:
        result = await self.booking_repository.get_user_bookings(
            user_id=user_id,
            **params.model_dump(exclude_none=True)
        )
        return PaginationResponse[BookingResponse].model_validate(
            result,
            from_attributes=True
        )

    async def get_user_booking(self, booking_id: int, user_id: int) -> BookingResponse:
        booking = await self.booking_repository.get_user_booking(booking_id=booking_id, user_id=user_id)
        if not booking:
            raise BookingNotFound
        return BookingResponse.model_validate(booking, from_attributes=True)

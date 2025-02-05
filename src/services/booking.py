from dataclasses import dataclass
from datetime import date, timedelta

from celery import Celery

from core.exceptions import (
    RoomNotFound,
    RoomAlreadyBooked,
    BookingNotFound,
    BookingCancelNotAllowed,
    BookingConfirmNotAllowed
)
from domain.repositories import IRoomRepository, IBookingRepository
from domain.services import IBookingService
from enums.status import Status
from schemas.booking import (
    BookingCreateRequest,
    BookingResponse,
    BookingCreateResponse,
    BookingParams
)
from schemas.response import PaginationResponse

__all__ = ("BookingService",)


@dataclass(frozen=True, slots=True)
class BookingService(IBookingService):
    room_repository: IRoomRepository
    booking_repository: IBookingRepository
    celery: Celery

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
            values=dict(
                user_id=user_id,
                room_id=schema.room_id,
                date_from=schema.date_from,
                date_to=schema.date_to
            )
        )
        self.celery.send_task(
            name="cancel_pending_booking",
            args=(booking.id, user_id),
            countdown=timedelta(minutes=15).seconds
        )
        return BookingCreateResponse.model_validate(booking, from_attributes=True)

    async def cancel_booking(self, booking_id: int, user_id: int) -> None:
        booking = await self.booking_repository.get_user_booking(booking_id=booking_id, user_id=user_id)
        if not booking:
            raise BookingNotFound
        if booking.status != Status.pending or booking.date_to <= date.today():
            raise BookingCancelNotAllowed
        await self.booking_repository.update_status(
            booking_id=booking_id,
            status=Status.canceled
        )

    async def confirm_booking(self, booking_id: int, user_id: int) -> None:
        booking = await self.get_user_booking(booking_id=booking_id, user_id=user_id)
        if booking.status != Status.pending:
            raise BookingConfirmNotAllowed(
                f"Confirmation of booking is not allowed. Current status: {booking.status}"
            )
        await self.booking_repository.update_status(
            booking_id=booking_id,
            status=Status.succeeded
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

    async def cancel_pending_booking(self, booking_id: int, user_id: int) -> None:
        booking = await self.get_user_booking(booking_id=booking_id, user_id=user_id)
        if booking.status == Status.pending:
            await self.booking_repository.update_status(
                booking_id=booking_id,
                status=Status.canceled
            )

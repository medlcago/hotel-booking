from dataclasses import dataclass
from datetime import date

from core.exceptions import BadRequestException, ForbiddenException
from repositories.booking import IBookingRepository
from repositories.room import IRoomRepository
from schemas.booking import BookingCreateRequest, BookingResponse, BookingCreateResponse
from schemas.pagination import PaginationResponse


@dataclass(frozen=True, slots=True)
class BookingService:
    room_repository: IRoomRepository
    booking_repository: IBookingRepository

    async def create_booking(self, schema: BookingCreateRequest, user_id: int) -> BookingCreateResponse:
        room = await self.room_repository.get_room_by_id(room_id=schema.room_id)
        if not room:
            raise BadRequestException
        room_booking = await self.booking_repository.get_room_booking(
            room_id=schema.room_id,
            date_from=schema.date_from,
            date_to=schema.date_to,
        )
        if room_booking:
            raise BadRequestException("Room already booked")

        result = await self.booking_repository.create_booking(
            values=dict(**schema.model_dump(), user_id=user_id, price_per_day=room.price_per_day)
        )
        return BookingCreateResponse.model_validate(result, from_attributes=True)

    async def cancel_booking(self, booking_id: int, user_id: int) -> None:
        booking = await self.booking_repository.get_user_booking(booking_id=booking_id, user_id=user_id)
        if not booking:
            raise BadRequestException("Booking not found")
        if not booking.status or booking.date_to <= date.today():
            raise ForbiddenException("You are not allowed to cancel this")
        await self.booking_repository.cancel_booking(booking_id=booking_id)

    async def get_bookings(self, user_id: int) -> PaginationResponse[BookingResponse]:
        result = await self.booking_repository.get_user_bookings(user_id=user_id)
        return PaginationResponse[BookingResponse].model_validate(
            result,
            from_attributes=True
        )

    async def get_booking(self, booking_id: int, user_id: int) -> BookingResponse:
        booking = await self.booking_repository.get_user_booking(booking_id=booking_id, user_id=user_id)
        if not booking:
            raise ForbiddenException
        return BookingResponse.model_validate(booking, from_attributes=True)

from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.booking.booking_repo import IBookingRepository, BookingRepository
from repositories.hotel.hotel_repo import IHotelRepository, HotelRepository
from repositories.review.review_repo import IReviewRepository, ReviewRepository
from repositories.room.room_repo import IRoomRepository, RoomRepository
from repositories.user.user_repo import IUserRepository, UserRepository


class IUnitOfWork(ABC):
    booking_repository: IBookingRepository
    hotel_repository: IHotelRepository
    review_repository: IReviewRepository
    room_repository: IRoomRepository
    user_repository: IUserRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.close()

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

        self.booking_repository = BookingRepository(session)
        self.hotel_repository = HotelRepository(session)
        self.review_repository = ReviewRepository(session)
        self.room_repository = RoomRepository(session)
        self.user_repository = UserRepository(session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()

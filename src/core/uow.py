from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.impl.booking_repo import BookingRepository
from repositories.impl.hotel_repo import HotelRepository
from repositories.impl.review_repo import ReviewRepository
from repositories.impl.room_repo import RoomRepository
from repositories.impl.user_repo import UserRepository

if TYPE_CHECKING:
    from repositories.booking_repo import IBookingRepository
    from repositories.hotel_repo import IHotelRepository
    from repositories.review_repo import IReviewRepository
    from repositories.room_repo import IRoomRepository
    from repositories.user_repo import IUserRepository


class IUnitOfWork(ABC):
    booking_repository: IBookingRepository
    hotel_repository: IHotelRepository
    review_repository: IReviewRepository
    room_repository: IRoomRepository
    user_repository: IUserRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.close()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

        self.booking_repository = BookingRepository(session)
        self.hotel_repository = HotelRepository(session)
        self.review_repository = ReviewRepository(session)
        self.room_repository = RoomRepository(session)
        self.user_repository = UserRepository(session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()

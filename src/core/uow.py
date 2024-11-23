from abc import abstractmethod, ABC
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.hotel import (
    IHotelRepository,
    HotelRepository
)
from repositories.review import (
    IReviewRepository,
    ReviewRepository
)
from repositories.room import (
    IRoomRepository,
    RoomRepository
)
from repositories.user import (
    IUserRepository,
    UserRepository
)


class IUnitOfWork(ABC):
    user_repository: IUserRepository
    hotel_repository: IHotelRepository
    room_repository: IRoomRepository
    review_repository: IReviewRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...

    @abstractmethod
    async def close(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.user_repository = UserRepository(session=self._session)  # type: ignore
        self.hotel_repository = HotelRepository(session=self._session)  # type: ignore
        self.room_repository = RoomRepository(session=self._session)  # type: ignore
        self.review_repository = ReviewRepository(session=self._session)  # type: ignore

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def close(self):
        await self._session.close()

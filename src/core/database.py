import logging
from contextlib import asynccontextmanager, AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

logger = logging.getLogger("hotel_booking")


class Database:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
            pool_timeout: int = 10
    ) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout
        )
        self.async_session = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        session = self.async_session()
        try:
            yield session
            await session.commit()
        except Exception as ex:
            logger.exception(f"Session rollback because of {ex}")
            await session.rollback()
            raise
        finally:
            await session.close()

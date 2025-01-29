from typing import ClassVar

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, async_scoped_session, AsyncSession

from core.db.context import SessionContext


class Session:
    _async_session_factory: ClassVar[async_sessionmaker[AsyncSession] | None] = None
    _scoped_session: ClassVar[async_scoped_session[AsyncSession] | None] = None
    _init: ClassVar[bool] = False

    @classmethod
    def initialize(cls, engine: AsyncEngine) -> None:
        cls._async_session_factory = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autoflush=False,
        )
        cls._scoped_session = async_scoped_session(
            cls._async_session_factory,
            scopefunc=SessionContext.get_session_context
        )
        cls._init = True

    @classmethod
    def get_session(cls) -> AsyncSession:
        if not cls._init:
            raise RuntimeError("session is not initialized. Please call Session.initialize()")
        return cls._scoped_session()

    @classmethod
    async def remove(cls) -> None:
        if not cls._init:
            raise RuntimeError("session is not initialized. Please call Session.initialize()")
        await cls._scoped_session.remove()

    @classmethod
    async def commit(cls):
        if not cls._init:
            raise RuntimeError("session is not initialized. Please call Session.initialize()")
        await cls._scoped_session.commit()

    @classmethod
    async def rollback(cls):
        if not cls._init:
            raise RuntimeError("session is not initialized. Please call Session.initialize()")
        await cls._scoped_session.rollback()

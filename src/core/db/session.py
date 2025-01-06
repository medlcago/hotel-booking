from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

from core.settings import settings

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engine = create_async_engine(
    url=settings.db.dsn,
    echo=settings.db.echo,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    pool_timeout=settings.db.pool_timeout
)

_async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)

session = async_scoped_session(
    _async_session_factory,
    scopefunc=get_session_context
)


@asynccontextmanager
async def session_scope(session_id: str):
    token = set_session_context(session_id)
    yield
    await session.remove()
    reset_session_context(token)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    yield session()

from contextlib import asynccontextmanager

from core.db.context import SessionContext
from core.db.session import Session


@asynccontextmanager
async def session_scope(session_id: str):
    try:
        token = SessionContext.set_session_context(session_id)
        yield
    finally:
        await Session.remove()
        SessionContext.reset_session_context(token)

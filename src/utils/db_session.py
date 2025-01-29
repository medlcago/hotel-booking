from sqlalchemy.ext.asyncio import AsyncEngine

from core.db.session import Session


def init_db_session(engine: AsyncEngine) -> None:
    Session.initialize(engine=engine)

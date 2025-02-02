from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class Engine:
    @classmethod
    def create(
            cls,
            url: str,
            **kwargs: Any
    ) -> AsyncEngine:
        return create_async_engine(
            url=url,
            **kwargs
        )

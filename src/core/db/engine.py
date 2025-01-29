from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class Engine:
    @classmethod
    def create(
            cls,
            url: str,
            echo: bool,
            pool_size: int,
            max_overflow: int,
            pool_timeout: int
    ) -> AsyncEngine:
        return create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout
        )

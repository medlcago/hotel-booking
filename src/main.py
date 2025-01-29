from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Depends

from api import init_api_router
from api.metrics import init_metrics
from core.container import Container
from core.exceptions import init_exception_handlers
from core.settings import settings
from middlewares import init_middlewares
from middlewares.throttling import Throttling
from utils.cache import init_cache
from utils.db_session import init_db_session


class APIServer:
    def __init__(self):
        self.container = Container()
        self.app = FastAPI(
            title="Hotel Booking API",
            lifespan=self.lifespan,
            debug=settings.debug,
            dependencies=[
                Depends(
                    Throttling(
                        limit=settings.default_throttle_limit,
                        throttle_time=settings.default_throttle_time
                    )
                )
            ]
        )
        self.app.container = self.container

    @asynccontextmanager
    async def lifespan(self, _: FastAPI) -> AsyncIterator[None]:
        init_db_session(
            engine=self.container.db_engine()
        )
        await init_cache(
            redis_url=str(settings.redis.url),
            prefix="fastapi-cache",
            expire=60,
        )
        yield

    def _build_app(self) -> FastAPI:
        init_middlewares(self.app)
        init_metrics(self.app)
        init_exception_handlers(self.app)
        init_api_router(self.app)

        return self.app

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        import uvicorn
        app = self._build_app()
        uvicorn.run(app, host=host, port=port, log_config=str(settings.log_config))


if __name__ == "__main__":
    server = APIServer()
    server.run()

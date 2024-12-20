from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from api import init_api_router
from api.metrics import init_metrics
from core.container import Container
from core.exceptions import init_exception_handlers
from core.settings import settings
from utils.cache import init_cache


class APIServer:
    def __init__(self):
        self.app = FastAPI(
            title="Hotel Booking API",
            lifespan=self.lifespan,
            debug=settings.debug
        )

        self.container = Container()
        self.app.container = self.container

    @asynccontextmanager
    async def lifespan(self, _: FastAPI) -> AsyncIterator[None]:
        await init_cache(
            redis_url=settings.redis.url,
            prefix="fastapi-cache",
            expire=60,
        )
        yield

    def _build_app(self) -> FastAPI:
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

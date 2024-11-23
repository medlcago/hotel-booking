from fastapi import APIRouter, FastAPI

from api.v1 import v1_router


def init_api_router(app: FastAPI) -> None:
    api_router = APIRouter(prefix="/api")
    api_router.include_router(v1_router)

    app.include_router(api_router)

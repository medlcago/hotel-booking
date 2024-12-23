from fastapi import APIRouter, FastAPI


def init_api_router(app: FastAPI) -> None:
    from api.v1 import v1_router

    api_router = APIRouter(prefix="/api")
    api_router.include_router(v1_router)

    app.include_router(api_router)

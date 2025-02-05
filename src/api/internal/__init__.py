from fastapi import APIRouter
from api.internal.events import router as events_router

internal_router = APIRouter(prefix="/_internal")
internal_router.include_router(events_router)

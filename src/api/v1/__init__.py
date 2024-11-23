from fastapi import APIRouter

from api.v1.auth import router as auth_router
from api.v1.hotels import router as hotels_router
from api.v1.reviews import router as reviews_router
from api.v1.rooms import router as rooms_router
from api.v1.users import router as users_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(hotels_router)
v1_router.include_router(rooms_router)
v1_router.include_router(reviews_router)

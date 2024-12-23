from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query
from fastapi_cache.decorator import cache

from api.deps import get_current_admin
from core.container import Container
from schemas.hotel import (
    HotelCreateRequest,
    HotelCreateResponse,
    HotelResponse,
    HotelParams,
    HotelUpdate
)
from schemas.response import PaginationResponse
from services.hotel_service import IHotelService

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.post(
    path="/",
    response_model=HotelCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden"
        },
    }
)
@inject
async def add_hotel(
        schema: HotelCreateRequest,
        hotel_service: IHotelService = Depends(Provide[Container.hotel_service])
):
    return await hotel_service.add_hotel(schema=schema)


@router.get(
    path="/{hotel_id}",
    response_model=HotelResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Hotel not found"
        },
    }
)
@cache(expire=60)
@inject
async def get_hotel_by_id(
        hotel_id: int,
        hotel_service: IHotelService = Depends(Provide[Container.hotel_service])
):
    return await hotel_service.get_hotel_by_id(hotel_id=hotel_id)


@router.get(
    path="/",
    response_model=PaginationResponse[HotelResponse]
)
@cache(expire=120)
@inject
async def get_hotels(
        params: Annotated[HotelParams, Query()],
        hotel_service: IHotelService = Depends(Provide[Container.hotel_service])
):
    return await hotel_service.get_hotels(params=params)


@router.patch(
    path="/{hotel_id}",
    response_model=HotelUpdate,
    dependencies=[Depends(get_current_admin)],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad request"
        }
    }
)
@inject
async def update_hotel(
        hotel_id: int,
        schema: HotelUpdate,
        hotel_service: IHotelService = Depends(Provide[Container.hotel_service])
):
    return await hotel_service.update_hotel(hotel_id=hotel_id, schema=schema)

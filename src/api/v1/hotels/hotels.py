from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query
from fastapi_cache.decorator import cache

from api.deps import get_current_admin_user
from core.container import Container
from schemas.hotel import HotelCreateRequest, HotelCreateResponse, HotelResponse, HotelParams
from schemas.pagination import PaginationResponse
from use_cases.hotel import IHotelUseCase

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.post(
    path="/",
    response_model=HotelCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Access denied"},
    }
)
@inject
async def add_hotel(
        schema: HotelCreateRequest,
        hotel_use_case: IHotelUseCase = Depends(Provide[Container.hotel_use_case])
):
    return await hotel_use_case.add_hotel(schema=schema)


@router.get(
    path="/{hotel_id}",
    response_model=HotelResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Hotel not found"}
    }
)
@cache(expire=60)
@inject
async def get_hotel_by_id(
        hotel_id: int,
        hotel_use_case: IHotelUseCase = Depends(Provide[Container.hotel_use_case])
):
    hotel = await hotel_use_case.get_hotel_by_id(hotel_id=hotel_id)
    return hotel


@router.get(
    path="/",
    response_model=PaginationResponse[HotelResponse]
)
@cache(expire=120)
@inject
async def get_hotels(
        params: Annotated[HotelParams, Query()],
        hotel_use_case: IHotelUseCase = Depends(Provide[Container.hotel_use_case]),
):
    return await hotel_use_case.get_hotels(
        params=params
    )

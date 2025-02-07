from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query
from fastapi_cache.decorator import cache

from api.deps import get_current_admin
from core.container import Container
from domain.usecases import IHotelUseCase
from schemas.hotel import (
    HotelCreateRequest,
    HotelCreateResponse,
    HotelResponse,
    HotelParams,
    HotelUpdate
)
from schemas.response import PaginationResponse, APIResponse

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.post(
    path="/",
    response_model=APIResponse[HotelCreateResponse],
    response_model_exclude_none=True,
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
        hotel_use_case: IHotelUseCase = Depends(Provide[Container.hotel_use_case])
):
    result = await hotel_use_case.add_hotel(schema=schema)
    return APIResponse(
        ok=True,
        result=result
    )


@router.get(
    path="/{hotel_id}",
    response_model=APIResponse[HotelResponse],
    response_model_exclude_none=True,
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
        hotel_use_case: IHotelUseCase = Depends(Provide[Container.hotel_use_case])
):
    result = await hotel_use_case.get_hotel_by_id(hotel_id=hotel_id)
    return APIResponse(
        ok=True,
        result=result
    )


@router.get(
    path="/",
    response_model=APIResponse[PaginationResponse[HotelResponse]],
    response_model_exclude_none=True,
)
@cache(expire=120)
@inject
async def get_hotels(
        params: Annotated[HotelParams, Query()],
        hotel_use_case: IHotelUseCase = Depends(Provide[Container.hotel_use_case])
):
    result = await hotel_use_case.get_hotels(params=params)
    return APIResponse(
        ok=True,
        result=result
    )


@router.patch(
    path="/{hotel_id}",
    response_model=APIResponse[HotelUpdate],
    response_model_exclude_none=True,
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
        hotel_use_case: IHotelUseCase = Depends(Provide[Container.hotel_use_case])
):
    result = await hotel_use_case.update_hotel(hotel_id=hotel_id, schema=schema)
    return APIResponse(
        ok=True,
        result=result
    )

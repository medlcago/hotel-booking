from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query
from fastapi_cache.decorator import cache

from api.deps import CurrentActiveUser, CurrentVerifiedUser
from core.container import Container
from domain.usecases import IBookingUseCase
from schemas.booking import (
    BookingCreateRequest,
    BookingResponse,
    BookingParams,
    BookingCancelRequest,
    BookingPaymentResponse
)
from schemas.response import PaginationResponse, APIResponse

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post(
    path="/",
    response_model=APIResponse[BookingPaymentResponse],
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad request",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        }
    }
)
@inject
async def create_booking(
        user: CurrentVerifiedUser,
        schema: BookingCreateRequest,
        booking_use_case: IBookingUseCase = Depends(Provide[Container.booking_use_case])
):
    result = await booking_use_case.create_booking(schema=schema, user_id=user.id)
    return APIResponse(
        ok=True,
        result=result
    )


@router.post(
    path="/cancel",
    response_model=APIResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad request",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden",
        }
    }
)
@inject
async def cancel_booking(
        user: CurrentActiveUser,
        schema: BookingCancelRequest,
        booking_use_case: IBookingUseCase = Depends(Provide[Container.booking_use_case])
):
    result = await booking_use_case.cancel_booking(schema=schema, user_id=user.id)
    return APIResponse(
        ok=True,
        result=result
    )


@router.get(
    path="/{booking_id}",
    response_model=APIResponse[BookingResponse],
    response_model_exclude_none=True,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden",
        }
    }
)
@cache(expire=300)
@inject
async def get_user_booking(
        user: CurrentActiveUser,
        booking_id: int,
        booking_use_case: IBookingUseCase = Depends(Provide[Container.booking_use_case])
):
    result = await booking_use_case.get_user_booking(booking_id=booking_id, user_id=user.id)
    return APIResponse(
        ok=True,
        result=result
    )


@router.get(
    path="/",
    response_model=APIResponse[PaginationResponse[BookingResponse]],
    response_model_exclude_none=True,
)
@cache(expire=300)
@inject
async def get_user_bookings(
        user: CurrentActiveUser,
        params: Annotated[BookingParams, Query()],
        booking_use_case: IBookingUseCase = Depends(Provide[Container.booking_use_case])
):
    result = await booking_use_case.get_user_bookings(user_id=user.id, params=params)
    return APIResponse(
        ok=True,
        result=result
    )

from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query
from fastapi_cache.decorator import cache

from api.deps import CurrentActiveUser, CurrentVerifiedUser
from core.container import Container
from domain.services import IBookingService
from schemas.booking import (
    BookingCreateRequest,
    BookingCreateResponse,
    BookingResponse,
    BookingParams,
    BookingCancelRequest
)
from schemas.response import PaginationResponse

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post(
    path="/",
    response_model=BookingCreateResponse,
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
        booking_service: IBookingService = Depends(Provide[Container.booking_service])
):
    return await booking_service.create_booking(schema=schema, user_id=user.id)


@router.post(
    path="/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
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
        booking_service: IBookingService = Depends(Provide[Container.booking_service])
):
    await booking_service.cancel_booking(schema=schema, user_id=user.id)


@router.get(
    path="/{booking_id}",
    response_model=BookingResponse,
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
        booking_service: IBookingService = Depends(Provide[Container.booking_service])
):
    return await booking_service.get_user_booking(booking_id=booking_id, user_id=user.id)


@router.get(
    path="/",
    response_model=PaginationResponse[BookingResponse]
)
@cache(expire=300)
@inject
async def get_user_bookings(
        user: CurrentActiveUser,
        params: Annotated[BookingParams, Query()],
        booking_service: IBookingService = Depends(Provide[Container.booking_service])
):
    return await booking_service.get_user_bookings(user_id=user.id, params=params)

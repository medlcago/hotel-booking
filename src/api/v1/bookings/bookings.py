from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends
from fastapi_cache.decorator import cache

from api.deps import CurrentUser
from core.container import Container
from schemas.booking import BookingCreateRequest, BookingCreateResponse, BookingResponse
from schemas.pagination import PaginationResponse
from use_cases.booking import IBookingUseCase

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=BookingCreateResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_booking(
        user: CurrentUser,
        schema: BookingCreateRequest,
        booking_use_case: IBookingUseCase = Depends(Provide[Container.booking_use_case])
):
    return await booking_use_case.create_booking(schema=schema, user_id=user.id)


@router.post("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def cancel_booking(
        user: CurrentUser,
        booking_id: int,
        booking_use_case: IBookingUseCase = Depends(Provide[Container.booking_use_case])
):
    await booking_use_case.cancel_booking(booking_id=booking_id, user_id=user.id)


@router.get("/{booking_id}", response_model=BookingResponse)
@cache(expire=300)
@inject
async def get_booking(
        user: CurrentUser,
        booking_id: int,
        booking_use_case: IBookingUseCase = Depends(Provide[Container.booking_use_case])
):
    return await booking_use_case.get_booking(booking_id=booking_id, user_id=user.id)


@router.get("/", response_model=PaginationResponse[BookingResponse])
@cache(expire=300)
@inject
async def get_bookings(
        user: CurrentUser,
        booking_use_case: IBookingUseCase = Depends(Provide[Container.booking_use_case])
):
    return await booking_use_case.get_bookings(user_id=user.id)

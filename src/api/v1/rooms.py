from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, status, Depends, Query
from fastapi_cache.decorator import cache

from api.deps import get_current_admin
from core.container import Container
from domain.usecases import IRoomUseCase
from schemas.response import PaginationResponse
from schemas.room import (
    RoomResponse,
    RoomCreateRequest,
    RoomCreateResponse,
    RoomParams,
    RoomUpdate
)

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post(
    path="/",
    response_model=RoomCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden"
        },
    }
)
@inject
async def add_room(
        schema: RoomCreateRequest,
        room_use_case: IRoomUseCase = Depends(Provide[Container.room_use_case])
):
    return await room_use_case.add_room(schema=schema)


@router.get(
    path="/{room_id}",
    response_model=RoomResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Room not found"
        },
    }
)
@cache(expire=60)
@inject
async def get_room_by_id(
        room_id: int,
        room_use_case: IRoomUseCase = Depends(Provide[Container.room_use_case])
):
    return await room_use_case.get_room_by_id(room_id=room_id)


@router.get(
    path="/",
    response_model=PaginationResponse[RoomResponse],
)
@cache(expire=120)
@inject
async def get_rooms(
        params: Annotated[RoomParams, Query()],
        room_use_case: IRoomUseCase = Depends(Provide[Container.room_use_case])
):
    return await room_use_case.get_rooms(params=params)


@router.patch(
    path="/{room_id}",
    response_model=RoomUpdate,
    dependencies=[Depends(get_current_admin)],
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden"
        }
    }
)
@inject
async def update_room(
        room_id: int,
        schema: RoomUpdate,
        room_use_case: IRoomUseCase = Depends(Provide[Container.room_use_case])
):
    return await room_use_case.update_room(room_id=room_id, schema=schema)

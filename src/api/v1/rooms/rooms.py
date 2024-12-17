from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, status, Depends, Query
from fastapi_cache.decorator import cache

from api.deps import get_current_admin
from core.container import ServiceContainer
from schemas.response import PaginationResponse
from schemas.room import (
    RoomResponse,
    RoomCreateRequest,
    RoomCreateResponse,
    RoomParams,
    RoomUpdate
)
from services.room import IRoomService

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
        room_service: IRoomService = Depends(Provide[ServiceContainer.room_service])
):
    return await room_service.add_room(schema=schema)


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
        room_service: IRoomService = Depends(Provide[ServiceContainer.room_service])
):
    return await room_service.get_room_by_id(room_id=room_id)


@router.get(
    path="/",
    response_model=PaginationResponse[RoomResponse],
)
@cache(expire=120)
@inject
async def get_rooms(
        params: Annotated[RoomParams, Query()],
        room_service: IRoomService = Depends(Provide[ServiceContainer.room_service])
):
    return await room_service.get_rooms(params=params)


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
        room_service: IRoomService = Depends(Provide[ServiceContainer.room_service])
):
    return await room_service.update_room(room_id=room_id, schema=schema)

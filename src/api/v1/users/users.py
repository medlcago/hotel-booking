from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query

from api.deps import CurrentUser, get_current_admin
from core.container import Container
from schemas.pagination import PaginationResponse
from schemas.user import UserResponse, UserParams
from use_cases.user import IUserUseCase

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="/me",
    response_model=UserResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Bad credentials",
        }
    }
)
@inject
async def get_me(user: CurrentUser):
    return user


@router.get(
    path="/",
    response_model=PaginationResponse[UserResponse],
    dependencies=[Depends(get_current_admin)],
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden",
        }
    }
)
@inject
async def get_users(
        params: Annotated[UserParams, Query()],
        user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case]),
):
    return await user_use_case.get_users(params=params)

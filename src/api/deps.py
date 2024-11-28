from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from core.container import Container
from core.exceptions import UnauthorizedException, ForbiddenException
from core.security import AccessTokenBearer, RefreshTokenBearer
from schemas.user import UserResponse
from services.user import IUserService

access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()


@inject
async def get_current_user(
        user_id: int = Depends(access_token_bearer),
        user_service: IUserService = Depends(Provide[Container.services.user_service])
) -> UserResponse:
    user = await user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise UnauthorizedException
    return user


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]


async def get_current_admin(user: CurrentUser) -> UserResponse:
    if not user.is_admin:
        raise ForbiddenException
    return user

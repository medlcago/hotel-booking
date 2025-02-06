from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, Request
from yookassa.domain.notification import WebhookNotification

from core.container import Container
from core.exceptions import (
    UnauthorizedException,
    ForbiddenException,
    UserInactive,
    UserNotVerified
)
from core.security import AccessTokenBearer, RefreshTokenBearer
from domain.usecases import IUserUseCase
from schemas.token import TokenResult
from schemas.user import UserResponse

access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()

AccessTokenResult = Annotated[TokenResult, Depends(access_token_bearer)]
RefreshTokenResult = Annotated[TokenResult, Depends(refresh_token_bearer)]


@inject
async def get_current_user(
        result: AccessTokenResult,
        user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case])
) -> UserResponse:
    user = await user_use_case.get_user_by_id(user_id=result.user_id)
    if not user:
        raise UnauthorizedException
    return user


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]


async def get_current_active_user(user: CurrentUser) -> UserResponse:
    if not user.is_active:
        raise UserInactive
    return user


CurrentActiveUser = Annotated[UserResponse, Depends(get_current_active_user)]


async def get_current_verified_user(user: CurrentActiveUser) -> UserResponse:
    if not user.is_verified:
        raise UserNotVerified
    return user


CurrentVerifiedUser = Annotated[UserResponse, Depends(get_current_verified_user)]


async def get_current_admin(user: CurrentUser) -> UserResponse:
    if not user.is_admin:
        raise ForbiddenException
    return user


CurrentAdmin = Annotated[UserResponse, Depends(get_current_admin)]


async def get_yookassa_webhook_notification(request: Request) -> WebhookNotification:
    event_json = await request.json()
    notification_object = WebhookNotification(event_json)
    if not (notification_object.event and notification_object.type and notification_object.object):
        raise ForbiddenException
    return notification_object


YookassaWebhookNotification = Annotated[WebhookNotification, Depends(get_yookassa_webhook_notification)]

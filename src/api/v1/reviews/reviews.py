from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query
from fastapi_cache.decorator import cache

from api.deps import CurrentActiveUser, CurrentVerifiedUser
from core.container import ServiceContainer
from schemas.response import PaginationResponse
from schemas.review import ReviewCreateRequest, ReviewCreateResponse, ReviewResponse, ReviewParams
from services.review import IReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewCreateResponse,
    response_model_exclude_none=True,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad request",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticated",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated",
        }
    }
)
@inject
async def add_review(
        schema: ReviewCreateRequest,
        user: CurrentVerifiedUser,
        review_service: IReviewService = Depends(Provide[ServiceContainer.review_service])
):
    return await review_service.add_review(schema=schema, user_id=user.id)


@router.get(
    path="/",
    response_model=PaginationResponse[ReviewResponse]
)
@cache(expire=120)
@inject
async def get_reviews(
        params: Annotated[ReviewParams, Query()],
        review_service: IReviewService = Depends(Provide[ServiceContainer.review_service])
):
    return await review_service.get_reviews(params=params)


@router.delete(
    path="/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden",
        }
    }
)
@inject
async def delete_review(
        review_id: int,
        user: CurrentActiveUser,
        review_service: IReviewService = Depends(Provide[ServiceContainer.review_service])
):
    await review_service.delete_review(review_id=review_id, user_id=user.id)

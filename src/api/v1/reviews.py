from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query
from fastapi_cache.decorator import cache

from api.deps import CurrentActiveUser, CurrentVerifiedUser
from core.container import Container
from domain.usecases import IReviewUseCase
from schemas.response import PaginationResponse, APIResponse
from schemas.review import ReviewCreateRequest, ReviewCreateResponse, ReviewResponse, ReviewParams

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[ReviewCreateResponse],
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
        review_use_case: IReviewUseCase = Depends(Provide[Container.review_use_case])
):
    result = await review_use_case.add_review(schema=schema, user_id=user.id)
    return APIResponse(
        ok=True,
        result=result
    )


@router.get(
    path="/",
    response_model=APIResponse[PaginationResponse[ReviewResponse]],
    response_model_exclude_none=True
)
@cache(expire=120)
@inject
async def get_reviews(
        params: Annotated[ReviewParams, Query()],
        review_use_case: IReviewUseCase = Depends(Provide[Container.review_use_case])
):
    result = await review_use_case.get_reviews(params=params)
    return APIResponse(
        ok=True,
        result=result
    )


@router.delete(
    path="/{review_id}",
    status_code=status.HTTP_200_OK,
    response_model=APIResponse,
    response_model_exclude_none=True,
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
        review_use_case: IReviewUseCase = Depends(Provide[Container.review_use_case])
):
    result = review_use_case.delete_review(review_id=review_id, user_id=user.id)
    return APIResponse(
        ok=True,
        result=result
    )

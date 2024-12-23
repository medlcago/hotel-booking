from dataclasses import dataclass

from core.exceptions import ReviewAlreadyExists, ReviewDeleteNotAllowed
from core.uow import IUnitOfWork
from repositories.base import AlreadyExistsError
from schemas.response import PaginationResponse
from schemas.review import (
    ReviewCreateRequest,
    ReviewResponse,
    ReviewCreateResponse,
    ReviewParams
)
from services.review_service import IReviewService

__all__ = ("ReviewService",)


@dataclass(frozen=True, slots=True)
class ReviewService(IReviewService):
    uow: IUnitOfWork

    async def add_review(self, schema: ReviewCreateRequest, user_id: int) -> ReviewCreateResponse:
        async with self.uow as uow:
            try:
                review = await uow.review_repository.add_review(dict(**schema.model_dump(), user_id=user_id))
                return ReviewCreateResponse.model_validate(review, from_attributes=True)
            except AlreadyExistsError:
                raise ReviewAlreadyExists

    async def get_reviews(self, params: ReviewParams) -> PaginationResponse[ReviewResponse]:
        async with self.uow as uow:
            result = await uow.review_repository.get_reviews(**params.model_dump(exclude_none=True))
            return PaginationResponse[ReviewResponse].model_validate(result, from_attributes=True)

    async def delete_review(self, review_id: int, user_id: int) -> None:
        async with self.uow as uow:
            review = await uow.review_repository.get_user_review(review_id=review_id, user_id=user_id)
            if not review:
                raise ReviewDeleteNotAllowed
            await uow.review_repository.delete_review(review_id=review_id, user_id=user_id)

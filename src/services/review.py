from dataclasses import dataclass

from core.exceptions import ReviewDeleteNotAllowed
from domain.repositories import IReviewRepository
from domain.services import IReviewService
from schemas.response import PaginationResponse
from schemas.review import (
    ReviewCreateRequest,
    ReviewResponse,
    ReviewCreateResponse,
    ReviewParams
)

__all__ = ("ReviewService",)


@dataclass(frozen=True, slots=True)
class ReviewService(IReviewService):
    review_repository: IReviewRepository

    async def add_review(self, schema: ReviewCreateRequest, user_id: int) -> ReviewCreateResponse:
        review = await self.review_repository.add_review(dict(**schema.model_dump(), user_id=user_id))
        return ReviewCreateResponse.model_validate(review, from_attributes=True)

    async def get_reviews(self, params: ReviewParams) -> PaginationResponse[ReviewResponse]:
        result = await self.review_repository.get_reviews(**params.model_dump(exclude_none=True))
        return PaginationResponse[ReviewResponse].model_validate(result, from_attributes=True)

    async def delete_review(self, review_id: int, user_id: int) -> None:
        review = await self.review_repository.get_user_review(review_id=review_id, user_id=user_id)
        if not review:
            raise ReviewDeleteNotAllowed
        await self.review_repository.delete_review(review_id=review_id, user_id=user_id)

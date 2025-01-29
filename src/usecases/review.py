from dataclasses import dataclass

from core.db.transactional import Transactional
from domain.services import IReviewService
from domain.usecases import IReviewUseCase
from schemas.response import PaginationResponse
from schemas.review import ReviewCreateRequest, ReviewCreateResponse, ReviewParams, ReviewResponse

__all__ = ("ReviewUseCase",)


@dataclass(frozen=True, slots=True)
class ReviewUseCase(IReviewUseCase):
    review_service: IReviewService

    @Transactional()
    async def add_review(self, schema: ReviewCreateRequest, user_id: int) -> ReviewCreateResponse:
        return await self.review_service.add_review(schema=schema, user_id=user_id)

    async def get_reviews(self, params: ReviewParams) -> PaginationResponse[ReviewResponse]:
        return await self.review_service.get_reviews(params=params)

    @Transactional()
    async def delete_review(self, review_id: int, user_id: int) -> None:
        return await self.review_service.delete_review(review_id=review_id, user_id=user_id)

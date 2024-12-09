from dataclasses import dataclass

from schemas.response import PaginationResponse
from schemas.review import ReviewCreateRequest, ReviewResponse, ReviewCreateResponse, ReviewParams
from services.review import IReviewService


@dataclass(frozen=True, slots=True)
class ReviewUseCase:
    review_service: IReviewService

    async def add_review(self, schema: ReviewCreateRequest, user_id: int) -> ReviewCreateResponse:
        return await self.review_service.add_review(schema=schema, user_id=user_id)

    async def get_reviews(self, params: ReviewParams) -> PaginationResponse[ReviewResponse]:
        return await self.review_service.get_reviews(params=params)

    async def delete_review(self, review_id: int, user_id: int) -> None:
        await self.review_service.delete_review(review_id=review_id, user_id=user_id)

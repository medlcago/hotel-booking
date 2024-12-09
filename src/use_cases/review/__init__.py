from typing import Protocol

from schemas.response import PaginationResponse
from schemas.review import ReviewCreateRequest, ReviewResponse, ReviewCreateResponse, ReviewParams
from .review_use_case import ReviewUseCase


class IReviewUseCase(Protocol):
    async def add_review(self, schema: ReviewCreateRequest, user_id: int) -> ReviewCreateResponse:
        ...

    async def get_reviews(self, params: ReviewParams) -> PaginationResponse[ReviewResponse]:
        ...

    async def delete_review(self, review_id: int, user_id: int) -> None:
        ...

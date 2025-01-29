from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.response import PaginationResponse
    from schemas.review import (
        ReviewCreateRequest,
        ReviewResponse,
        ReviewCreateResponse,
        ReviewParams
    )


class IReviewUseCase(ABC):
    @abstractmethod
    async def add_review(self, schema: ReviewCreateRequest, user_id: int) -> ReviewCreateResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_reviews(self, params: ReviewParams) -> PaginationResponse[ReviewResponse]:
        raise NotImplementedError

    @abstractmethod
    async def delete_review(self, review_id: int, user_id: int) -> None:
        raise NotImplementedError

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Review
    from repositories.base import Result
    from schemas.filters import SortOrderType


class IReviewRepository(ABC):
    @abstractmethod
    async def add_review(self, values: dict[str, Any]) -> Review:
        raise NotImplementedError

    @abstractmethod
    async def get_reviews(
            self,
            limit: int,
            offset: int,
            field: str = "id",
            sort_order: SortOrderType = "asc",
            **kwargs,
    ) -> Result[Review]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_review(self, review_id: int, user_id: int) -> Review | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_review(self, review_id: int, user_id: int) -> None:
        raise NotImplementedError

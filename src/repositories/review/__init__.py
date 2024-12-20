from abc import ABC
from typing import Any

from models import Review
from repositories.base import Result
from schemas.filters import SortOrderType


class IReviewRepository(ABC):
    async def add_review(self, values: dict[str, Any]) -> Review:
        ...

    async def get_reviews(
            self,
            limit: int,
            offset: int,
            field: str = "id",
            sort_order: SortOrderType = "asc",
            **kwargs,
    ) -> Result[Review]:
        ...

    async def get_user_review(self, review_id: int, user_id: int) -> Review | None:
        ...

    async def delete_review(self, review_id: int, user_id: int) -> None:
        ...

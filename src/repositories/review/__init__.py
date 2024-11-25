from typing import Protocol, Any, Literal

from models import Review
from repositories.base import Result
from .review_repo import ReviewRepository


class IReviewRepository(Protocol):
    async def add_review(self, values: dict[str, Any]) -> Review:
        ...

    async def get_reviews(
            self,
            limit: int,
            offset: int,
            sort_order: Literal["asc", "desc"],
            **kwargs,
    ) -> Result[Any]:
        ...

    async def get_user_review(self, review_id: int, user_id: int) -> Review | None:
        ...

    async def delete_review(self, review_id: int, user_id: int) -> None:
        ...

from typing import Any

from sqlalchemy import insert, select, func, delete
from sqlalchemy.exc import IntegrityError

from core.exceptions import ReviewAlreadyExists
from domain.entities import Review
from domain.repositories import IReviewRepository
from domain.repositories.base import Repository
from schemas.filters import SortOrder
from schemas.response import PaginationResponse

__all__ = ("ReviewRepository",)


class ReviewRepository(IReviewRepository, Repository[Review]):
    table = Review

    async def add_review(self, values: dict[str, Any]) -> Review:
        review_stmt = (
            insert(self.table).
            values(**values).
            returning(self.table)
        )
        try:
            return await self.session.scalar(review_stmt)
        except IntegrityError:
            raise ReviewAlreadyExists

    async def get_reviews(
            self,
            limit: int,
            offset: int,
            field: str = "id",
            sort_order: SortOrder = "asc",
            **kwargs,
    ) -> PaginationResponse[Review]:
        reviews_stmt = (
            select(self.table).
            limit(limit).
            offset(offset).
            filter_by(**kwargs)
        )
        column = getattr(self.table, field, None)
        if column:
            reviews_stmt = reviews_stmt.order_by(column.desc() if sort_order == "desc" else column.asc())
        count_stmt = (
            select(func.count(self.table.id)).
            filter_by(**kwargs)
        )
        reviews = (await self.session.scalars(reviews_stmt)).all()
        count = await self.session.scalar(count_stmt)
        return PaginationResponse(
            count=count,
            items=reviews,
        )

    async def get_user_review(self, review_id: int, user_id: int) -> Review | None:
        review_stmt = (
            select(self.table).
            filter_by(id=review_id, user_id=user_id)
        )
        return await self.session.scalar(review_stmt)

    async def delete_review(self, review_id: int, user_id: int) -> None:
        review_stmt = (
            delete(self.table).
            filter_by(id=review_id, user_id=user_id)
        )
        await self.session.execute(review_stmt)

from typing import Any

from sqlalchemy import insert, select, func, delete
from sqlalchemy.exc import IntegrityError

from models import Review
from repositories.base import Repository, AlreadyExistsError, Result
from repositories.review import IReviewRepository
from schemas.filters import SortOrderType

__all__ = ("ReviewRepository", "IReviewRepository")


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
            raise AlreadyExistsError

    async def get_reviews(
            self,
            limit: int,
            offset: int,
            field: str = "id",
            sort_order: SortOrderType = "asc",
            **kwargs,
    ) -> Result[Review]:
        reviews_stmt = (
            select(self.table).
            limit(limit).
            offset(offset).
            filter_by(**kwargs)
        )
        if column := getattr(self.table, field, None):
            reviews_stmt = reviews_stmt.order_by(
                column.desc() if sort_order == "desc" else column.asc()  # noqa
            )
        count_stmt = (
            select(func.count(self.table.id)).
            filter_by(**kwargs)
        )

        reviews = (await self.session.scalars(reviews_stmt)).all()
        count = await self.session.scalar(count_stmt)
        return Result(
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

from typing import Any

from sqlalchemy import insert, select, func, delete
from sqlalchemy.exc import IntegrityError

from core.db.session import get_session
from models import Review
from repositories.base import Repository, AlreadyExistsError, Result
from repositories.review_repo import IReviewRepository
from schemas.filters import SortOrderType

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
            async with get_session() as session:
                return await session.scalar(review_stmt)
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
        async with get_session() as session:
            reviews = (await session.scalars(reviews_stmt)).all()
            count = await session.scalar(count_stmt)
            return Result(
                count=count,
                items=reviews,
            )

    async def get_user_review(self, review_id: int, user_id: int) -> Review | None:
        review_stmt = (
            select(self.table).
            filter_by(id=review_id, user_id=user_id)
        )
        async with get_session() as session:
            return await session.scalar(review_stmt)

    async def delete_review(self, review_id: int, user_id: int) -> None:
        review_stmt = (
            delete(self.table).
            filter_by(id=review_id, user_id=user_id)
        )
        async with get_session() as session:
            await session.execute(review_stmt)

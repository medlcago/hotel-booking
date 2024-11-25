from typing import Any, Literal

from sqlalchemy import insert, select, func, delete
from sqlalchemy.exc import IntegrityError

from models import Review
from repositories.base import Repository, AlreadyExistsError, Result


class ReviewRepository(Repository[Review]):
    table = Review

    async def add_review(self, values: dict[str, Any]) -> Review:
        review_stmt = insert(self.table).values(**values).returning(self.table)
        try:
            async with self.session_factory() as session:
                return await session.scalar(review_stmt)
        except IntegrityError:
            raise AlreadyExistsError

    async def get_reviews(
            self,
            limit: int,
            offset: int,
            sort_order: Literal["asc", "desc"],
            **kwargs,
    ) -> Result[Review]:
        reviews_stmt = (
            select(self.table).
            limit(limit).
            offset(offset).
            filter_by(**kwargs).
            order_by(self.table.created_at.desc() if sort_order == "desc" else self.table.created_at.asc())
        )
        count_stmt = select(func.count(self.table.id)).filter_by(**kwargs)

        async with self.session_factory() as session:
            reviews = (await session.scalars(reviews_stmt)).all()
            count = await session.scalar(count_stmt)
            return Result(
                count=count,
                items=reviews,
            )

    async def get_user_review(self, review_id: int, user_id: int) -> Review | None:
        review_stmt = select(self.table).filter_by(id=review_id, user_id=user_id)
        async with self.session_factory() as session:
            return await session.scalar(review_stmt)

    async def delete_review(self, review_id: int, user_id: int) -> None:
        review_stmt = delete(self.table).filter_by(id=review_id, user_id=user_id)
        async with self.session_factory() as session:
            await session.execute(review_stmt)

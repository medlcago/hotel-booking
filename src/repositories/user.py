from typing import Any

from sqlalchemy import insert, select, func, update

from domain.entities import User
from domain.repositories import IUserRepository
from domain.repositories.base import Repository
from schemas.response import PaginationResponse

__all__ = ("UserRepository",)


class UserRepository(IUserRepository, Repository[User]):
    table = User

    async def create_user(self, values: dict[str, Any]) -> User:
        user_stmt = (
            insert(self.table).
            values(**values).
            returning(self.table)
        )
        return await self.session.scalar(user_stmt)

    async def get_user_by_id(self, user_id: int) -> User | None:
        user_stmt = (
            select(self.table).
            filter_by(id=user_id)
        )
        return await self.session.scalar(user_stmt)

    async def get_user_by_email(self, email: str) -> User | None:
        user_stmt = (
            select(self.table).
            filter_by(email=email)
        )
        return await self.session.scalar(user_stmt)

    async def get_users(self, limit: int, offset: int, **kwargs) -> PaginationResponse[User]:
        users_stmt = (
            select(self.table).
            limit(limit).
            offset(offset).
            filter_by(**kwargs)
        )
        count_stmt = (
            select(func.count(self.table.id)).
            filter_by(**kwargs)
        )

        users = (await self.session.scalars(users_stmt)).all()
        count = await self.session.scalar(count_stmt)
        return PaginationResponse(
            count=count,
            items=users
        )

    async def update_user(self, user_id: int, values: dict[str, Any]) -> User | None:
        user_stmt = (
            update(self.table).
            filter_by(id=user_id).
            values(**values).
            returning(self.table)
        )
        return await self.session.scalar(user_stmt)

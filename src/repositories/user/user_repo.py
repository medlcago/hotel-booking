from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from models import User
from repositories.base import Repository, AlreadyExistsError


class UserRepository(Repository[User]):
    table = User

    async def create_user(self, values: dict[str, Any]) -> User:
        try:
            user_stmt = insert(self.table).values(**values).returning(self.table)
            return await self.session.scalar(user_stmt)
        except IntegrityError:
            raise AlreadyExistsError

    async def get_user_by_id(self, user_id: int) -> User | None:
        user_stmt = select(self.table).filter_by(id=user_id)
        return await self.session.scalar(user_stmt)

    async def get_user_by_email(self, email: str) -> User | None:
        user_stmt = select(self.table).filter_by(email=email)
        return await self.session.scalar(user_stmt)

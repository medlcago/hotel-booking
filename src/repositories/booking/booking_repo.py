from sqlalchemy import select, func

from models import Booking
from repositories.base import Repository, Result


class BookingRepository(Repository[Booking]):
    table = Booking

    async def get_user_bookings(self, user_id: int, **kwargs) -> Result[Booking]:
        bookings_stmt = select(self.table).filter_by(user_id=user_id, **kwargs)
        count_stmt = select(func.count(self.table.id)).filter_by(**kwargs)

        bookings = (await self.session.scalars(bookings_stmt)).all()
        count = await self.session.scalar(count_stmt)
        return Result(
            count=count,
            items=bookings
        )

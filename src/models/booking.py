from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models import User
    from models import Room


class Booking(Base):
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[datetime]
    date_to: Mapped[datetime]
    price_per_day: Mapped[Decimal]
    status: Mapped[bool] = mapped_column(default=True, server_default="1")

    user: Mapped[User] = relationship(back_populates="bookings")
    room: Mapped[Room] = relationship(back_populates="bookings")

    @hybrid_property
    def total_days(self) -> int:
        return (self.date_to - self.date_from).days

    @hybrid_property
    def total_cost(self) -> Decimal:
        return self.total_days * self.price_per_day
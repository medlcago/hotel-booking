from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.base import Base, TimeStampMixin

if TYPE_CHECKING:
    from domain.entities import User
    from domain.entities import Room


class Booking(Base, TimeStampMixin):
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    status: Mapped[str] = mapped_column(String(20), default="pending", server_default="pending")

    user: Mapped[User] = relationship(back_populates="bookings")
    room: Mapped[Room] = relationship(back_populates="bookings", lazy="joined")

    @hybrid_property
    def total_days(self) -> int:
        return (self.date_to - self.date_from).days

    @hybrid_property
    def price_per_day(self) -> Decimal:
        return self.room.price_per_day

    @hybrid_property
    def total_cost(self) -> Decimal:
        return self.total_days * self.price_per_day

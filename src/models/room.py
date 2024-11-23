from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimeStampMixin

if TYPE_CHECKING:
    from models import Hotel
    from models import Booking


class Room(Base, TimeStampMixin):
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(150))
    room_type: Mapped[str] = mapped_column(String(32))
    price_per_day: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    description: Mapped[str | None] = mapped_column(String(500))

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    bookings: Mapped[list[Booking]] = relationship(back_populates="room")

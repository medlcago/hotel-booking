from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property

from models.base import Base, TimeStampMixin
from models.review import Review

if TYPE_CHECKING:
    from models import Room


class Hotel(Base, TimeStampMixin):
    name: Mapped[str] = mapped_column(String(150))
    location: Mapped[str] = mapped_column(String(300))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(String(500))

    rooms: Mapped[list[Room]] = relationship(back_populates="hotel")
    reviews: Mapped[list[Review]] = relationship(back_populates="hotel")


Hotel.rating = column_property(
    select(func.round(func.coalesce(func.avg(Review.score), 0), 1))
    .where(Review.hotel_id == Hotel.id)
    .correlate_except(Review)
    .scalar_subquery(),
    deferred=True
)

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.base import Base, TimeStampMixin

if TYPE_CHECKING:
    from domain.entities import Review
    from domain.entities import Booking


class User(Base, TimeStampMixin):
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(300), unique=True)
    password: Mapped[str] = mapped_column(String(60))
    phone: Mapped[str | None] = mapped_column(String(20))
    date_of_birth: Mapped[date | None]
    loyalty_points: Mapped[int] = mapped_column(default=0, server_default="0")
    is_active: Mapped[bool] = mapped_column(default=True, server_default="1")
    is_verified: Mapped[bool] = mapped_column(default=False, server_default="0")
    is_admin: Mapped[bool] = mapped_column(default=False, server_default="0")

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    reviews: Mapped[list[Review]] = relationship(back_populates="user")
    bookings: Mapped[list[Booking]] = relationship(back_populates="user")

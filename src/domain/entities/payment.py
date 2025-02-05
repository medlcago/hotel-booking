from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.base import Base, TimeStampMixin

if TYPE_CHECKING:
    from domain.entities import Booking
    from domain.entities import User


class Payment(Base, TimeStampMixin):
    payment_id: Mapped[str] = mapped_column(String(100))
    payment_method: Mapped[str] = mapped_column(String(60))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    currency: Mapped[str] = mapped_column(String(3))
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    booking: Mapped[Booking] = relationship(back_populates="payment")
    user: Mapped[User] = relationship(back_populates="payments")

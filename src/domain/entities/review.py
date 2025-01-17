from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, CheckConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.base import Base, TimeStampMixin

if TYPE_CHECKING:
    from domain.entities import Hotel
    from domain.entities import User


class Review(Base, TimeStampMixin):
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    score: Mapped[int]
    comment: Mapped[str | None] = mapped_column(String(255))

    __table_args__ = (
        CheckConstraint("score >= 1 and score <= 5", name="rating_score_check"),
        UniqueConstraint("user_id", "hotel_id", name="rating_user_id"),
    )

    hotel: Mapped[Hotel] = relationship(back_populates="reviews")
    user: Mapped[User] = relationship(back_populates="reviews")

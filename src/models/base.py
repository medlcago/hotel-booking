from datetime import datetime

from sqlalchemy import func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from core.settings import settings


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls):  # noqa
        return f"{cls.__name__.lower()}s"


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now()
    )

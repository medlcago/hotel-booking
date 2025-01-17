from datetime import datetime

from sqlalchemy import func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

_naming_convention: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    metadata = MetaData(
        naming_convention=_naming_convention,
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

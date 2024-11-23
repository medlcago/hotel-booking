from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar, Collection, Annotated

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

T = TypeVar("T", bound=BaseModel)

FilterTypes: TypeAlias = "CollectionFilter[Any] | LimitOffset | OrderBy | SearchFilter | NotInCollectionFilter[Any] | NotInSearchFilter"
"""Aggregate type alias of the types supported for collection filtering."""


@dataclass
class CollectionFilter(Generic[T]):
    """Data required to construct a ``WHERE ... IN (...)`` clause."""

    field_name: str
    """Name of the model attribute to filter on."""
    values: Collection[T]
    """Values for ``IN`` clause."""


@dataclass
class NotInCollectionFilter(Generic[T]):
    """Data required to construct a ``WHERE ... NOT IN (...)`` clause."""

    field_name: str
    """Name of the model attribute to filter on."""
    values: Collection[T]
    """Values for ``NOT IN`` clause."""


class LimitOffset(BaseModel):
    """Data required to add limit/offset filtering to a query."""

    limit: Annotated[int, Field(ge=1)] = 10
    """Value for ``LIMIT`` clause of query."""
    offset: Annotated[int, Field(ge=0)] = 0
    """Value for ``OFFSET`` clause of query."""


@dataclass
class OrderBy:
    """Data required to construct a ``ORDER BY ...`` clause."""

    field_name: str
    """Name of the model attribute to sort on."""
    sort_order: Literal["asc", "desc"] = "asc"
    """Sort ascending or descending"""


@dataclass
class SearchFilter:
    """Data required to construct a ``WHERE field_name LIKE '%' || :value || '%'`` clause."""

    field_name: str
    """Name of the model attribute to sort on."""
    value: str
    """Values for ``LIKE`` clause."""
    ignore_case: bool | None = False
    """Should the search be case insensitive."""


@dataclass
class NotInSearchFilter:
    """Data required to construct a ``WHERE field_name NOT LIKE '%' || :value || '%'`` clause."""

    field_name: str
    """Name of the model attribute to search on."""
    value: str
    """Values for ``NOT LIKE`` clause."""
    ignore_case: bool | None = False
    """Should the search be case insensitive."""

from __future__ import annotations

from typing import TypeVar, Literal

from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
SortOrderType = Literal["asc", "desc"]

from typing import Sequence

from pydantic import BaseModel, ConfigDict


class PaginationResponse[T](BaseModel):
    count: int
    items: Sequence[T]

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


class Message(BaseModel):
    message: str

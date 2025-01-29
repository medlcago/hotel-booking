from enum import StrEnum, auto


class Status(StrEnum):
    pending = auto()
    succeeded = auto()
    canceled = auto()

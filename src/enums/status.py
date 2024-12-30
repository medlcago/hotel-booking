from enum import StrEnum, auto


class BookingStatus(StrEnum):
    pending = auto()
    confirmed = auto()
    canceled = auto()

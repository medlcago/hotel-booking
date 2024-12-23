from enum import StrEnum, auto


class PaymentStatus(StrEnum):
    pending = auto()
    paid = auto()
    canceled = auto()
    refund = auto()

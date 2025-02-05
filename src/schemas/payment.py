from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from enums.currency import Currency
from enums.payment import PaymentMethod


class PaymentResponse(BaseModel):
    id: int
    payment_id: str
    payment_method: PaymentMethod
    amount: Decimal
    currency: Currency
    booking_id: int
    user_id: int
    created_at: datetime


class PaymentCreateResponse(PaymentResponse):
    payment_url: str

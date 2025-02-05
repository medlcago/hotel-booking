from .booking import IBookingRepository
from .hotel import IHotelRepository
from .payment import IPaymentRepository
from .review import IReviewRepository
from .room import IRoomRepository
from .user import IUserRepository

__all__ = (
    "IBookingRepository",
    "IHotelRepository",
    "IReviewRepository",
    "IRoomRepository",
    "IUserRepository",
    "IPaymentRepository",
)

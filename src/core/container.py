from dependency_injector import containers, providers

from core.database import Database
from core.settings import settings
from core.uow import UnitOfWork
from services.auth import AuthService
from services.booking import BookingService
from services.hotel import HotelService
from services.review import ReviewService
from services.room import RoomService
from services.user import UserService
from stores.redis import RedisStore


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.auth.auth",
            "api.v1.users.users",
            "api.v1.hotels.hotels",
            "api.v1.rooms.rooms",
            "api.v1.reviews.reviews",
            "api.v1.bookings.bookings",
            "api.deps",
            "utils.cache",
        ]
    )

    db = providers.Singleton(
        Database,
        url=settings.db.dsn,
        echo=settings.db.echo,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
        pool_timeout=settings.db.pool_timeout
    )

    uow = providers.Factory(
        UnitOfWork,
        session=db.provided.session
    )

    redis_store = providers.Singleton(
        RedisStore.with_client,
        url=settings.redis.url
    )

    user_service = providers.Factory(
        UserService,
        uow=uow,
    )

    hotel_service = providers.Factory(
        HotelService,
        uow=uow,
    )

    room_service = providers.Factory(
        RoomService,
        uow=uow,
    )

    auth_service = providers.Factory(
        AuthService,
        uow=uow,
        store=redis_store,
    )

    review_service = providers.Factory(
        ReviewService,
        uow=uow,
    )

    booking_service = providers.Factory(
        BookingService,
        uow=uow,
    )

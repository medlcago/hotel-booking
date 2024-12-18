from dependency_injector import containers, providers
from redis.asyncio import Redis

from core.database import Database
from core.settings import settings
from repositories.booking import BookingRepository
from repositories.hotel import HotelRepository
from repositories.review import ReviewRepository
from repositories.room import RoomRepository
from repositories.user import UserRepository
from services.auth import AuthService
from services.booking import BookingService
from services.hotel import HotelService
from services.review import ReviewService
from services.room import RoomService
from services.user import UserService
from stores.redis import RedisStore


class RepositoryContainer(containers.DeclarativeContainer):
    db = providers.Singleton(
        Database,
        url=settings.db.dsn,
        echo=settings.db.echo,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
        pool_timeout=settings.db.pool_timeout
    )

    booking_repository = providers.Factory(
        BookingRepository,
        session_factory=db.provided.session
    )

    hotel_repository = providers.Factory(
        HotelRepository,
        session_factory=db.provided.session
    )

    review_repository = providers.Factory(
        ReviewRepository,
        session_factory=db.provided.session
    )

    room_repository = providers.Factory(
        RoomRepository,
        session_factory=db.provided.session
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session
    )


class ServiceContainer(containers.DeclarativeContainer):
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

    repositories = providers.Container(
        RepositoryContainer,
    )

    redis = providers.Singleton(
        Redis.from_url,
        url=settings.redis.url,
    )

    redis_store = providers.Singleton(
        RedisStore,
        redis=redis
    )

    user_service = providers.Factory(
        UserService,
        user_repository=repositories.user_repository,
    )

    hotel_service = providers.Factory(
        HotelService,
        hotel_repository=repositories.hotel_repository,
    )

    room_service = providers.Factory(
        RoomService,
        room_repository=repositories.room_repository,
    )

    auth_service = providers.Factory(
        AuthService,
        user_repository=repositories.user_repository,
        store=redis_store
    )

    review_service = providers.Factory(
        ReviewService,
        review_repository=repositories.review_repository,
    )

    booking_service = providers.Factory(
        BookingService,
        booking_repository=repositories.booking_repository,
        room_repository=repositories.room_repository,
    )

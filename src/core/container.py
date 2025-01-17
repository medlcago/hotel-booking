from dependency_injector import containers, providers

from core.settings import settings
from repositories.booking import BookingRepository
from repositories.hotel import HotelRepository
from repositories.review import ReviewRepository
from repositories.room import RoomRepository
from repositories.user import UserRepository
from services.auth import AuthService
from services.booking import BookingService
from services.email import EmailService
from services.hotel import HotelService
from services.review import ReviewService
from services.room import RoomService
from services.user import UserService
from stores.redis import RedisStore


class RepositoriesContainer(containers.DeclarativeContainer):
    booking_repository = providers.Singleton(BookingRepository)
    hotel_repository = providers.Singleton(HotelRepository)
    review_repository = providers.Singleton(ReviewRepository)
    room_repository = providers.Singleton(RoomRepository)
    user_repository = providers.Singleton(UserRepository)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "utils.cache",
        ],
        packages=[
            "middlewares",
            "api",
            "api.v1"
        ]
    )

    repositories = providers.Container(RepositoriesContainer)

    redis_store = providers.Singleton(
        RedisStore.with_client,
        url=str(settings.redis.url)
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
        store=redis_store,
    )

    review_service = providers.Factory(
        ReviewService,
        review_repository=repositories.review_repository,
    )

    booking_service = providers.Factory(
        BookingService,
        room_repository=repositories.room_repository,
        booking_repository=repositories.booking_repository,
    )

    email_service = providers.Factory(
        EmailService,
        smtp_server=settings.smtp_server.host,
        smtp_port=settings.smtp_server.port,
        smtp_user=settings.smtp_server.username,
        smtp_password=settings.smtp_server.password,
    )

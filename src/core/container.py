from dependency_injector import containers, providers

from core.settings import settings
from repositories.impl.booking_repo import BookingRepository
from repositories.impl.hotel_repo import HotelRepository
from repositories.impl.review_repo import ReviewRepository
from repositories.impl.room_repo import RoomRepository
from repositories.impl.user_repo import UserRepository
from services.impl.auth_service import AuthService
from services.impl.booking_service import BookingService
from services.impl.email_service import EmailService
from services.impl.hotel_service import HotelService
from services.impl.review_service import ReviewService
from services.impl.room_service import RoomService
from services.impl.user_service import UserService
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

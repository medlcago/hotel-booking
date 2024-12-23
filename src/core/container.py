from dependency_injector import containers, providers

from core.database import Database
from core.settings import settings
from core.uow import UnitOfWork
from services.impl.auth_service import AuthService
from services.impl.booking_service import BookingService
from services.impl.email_service import EmailService
from services.impl.hotel_service import HotelService
from services.impl.review_service import ReviewService
from services.impl.room_service import RoomService
from services.impl.user_service import UserService
from stores.redis import RedisStore


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

    email_service = providers.Factory(
        EmailService,
        smtp_server=settings.smtp_server.host,
        smtp_port=settings.smtp_server.port,
        smtp_user=settings.smtp_server.username,
        smtp_password=settings.smtp_server.password,
    )

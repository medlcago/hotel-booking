from dependency_injector import containers, providers

from core.db.engine import Engine
from core.db.session import Session
from core.settings import settings
from repositories import (
    BookingRepository,
    HotelRepository,
    PaymentRepository,
    ReviewRepository,
    RoomRepository,
    UserRepository
)
from services import (
    AuthService,
    BookingService,
    EmailService,
    HotelService,
    ReviewService,
    RoomService,
    UserService,
    YookassaService
)
from stores.redis import RedisStore
from usecases import (
    AuthUseCase,
    BookingUseCase,
    RoomUseCase,
    UserUseCase, HotelUseCase, ReviewUseCase
)
from utils.celery_utils import create_celery


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "middlewares",
            "api",
            "api.v1",
            "utils",
        ]
    )

    db_engine = providers.Singleton(
        Engine.create,
        url=settings.db.dsn,
        echo=settings.db.echo,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
        pool_timeout=settings.db.pool_timeout,
    )

    db_session = providers.Factory(
        Session.get_session,
    )

    booking_repository = providers.Factory(
        BookingRepository,
        session=db_session
    )
    hotel_repository = providers.Factory(
        HotelRepository,
        session=db_session
    )
    review_repository = providers.Factory(
        ReviewRepository,
        session=db_session
    )
    room_repository = providers.Factory(
        RoomRepository,
        session=db_session
    )
    user_repository = providers.Factory(
        UserRepository,
        session=db_session
    )
    payment_repository = providers.Factory(
        PaymentRepository,
        session=db_session
    )

    celery_app = providers.Singleton(
        create_celery,
        broker_url=settings.celery.broker_url,
        backend_url=settings.celery.backend_url,
        timezone="UTC",
        enable_utc=True,
        broker_connection_retry_on_startup=True
    )

    redis_store = providers.Singleton(
        RedisStore.with_client,
        url=str(settings.redis.url)
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        celery=celery_app
    )

    hotel_service = providers.Factory(
        HotelService,
        hotel_repository=hotel_repository,
    )

    room_service = providers.Factory(
        RoomService,
        room_repository=room_repository,
    )

    auth_service = providers.Factory(
        AuthService,
        user_repository=user_repository,
        store=redis_store,
        celery=celery_app
    )

    review_service = providers.Factory(
        ReviewService,
        review_repository=review_repository,
    )

    booking_service = providers.Factory(
        BookingService,
        room_repository=room_repository,
        booking_repository=booking_repository,
        celery=celery_app
    )

    email_service = providers.Singleton(
        EmailService,
        smtp_server=settings.smtp_server.host,
        smtp_port=settings.smtp_server.port,
        smtp_user=settings.smtp_server.username,
        smtp_password=settings.smtp_server.password,
    )

    yookassa_service = providers.Factory(
        YookassaService,
        shop_id=settings.yookassa.shop_id,
        secret_key=settings.yookassa.secret_key,
        payment_repository=payment_repository
    )

    auth_use_case = providers.Factory(
        AuthUseCase,
        auth_service=auth_service,
    )

    user_use_case = providers.Factory(
        UserUseCase,
        user_service=user_service,
    )

    booking_use_case = providers.Factory(
        BookingUseCase,
        booking_service=booking_service,
        payment_service=yookassa_service
    )

    room_use_case = providers.Factory(
        RoomUseCase,
        room_service=room_service,
    )

    hotel_use_case = providers.Factory(
        HotelUseCase,
        hotel_service=hotel_service,
    )

    review_use_case = providers.Factory(
        ReviewUseCase,
        review_service=review_service
    )

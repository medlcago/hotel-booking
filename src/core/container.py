from dependency_injector import containers, providers

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
from use_cases.auth import AuthUseCase
from use_cases.booking import BookingUseCase
from use_cases.hotel import HotelUseCase
from use_cases.review import ReviewUseCase
from use_cases.room import RoomUseCase
from use_cases.user import UserUseCase


class RepositoryContainer(containers.DeclarativeContainer):
    db = providers.Singleton(
        Database,
        url=settings.db.dsn,
        echo=settings.debug,
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
    repositories = providers.Container(
        RepositoryContainer,
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
    )

    review_service = providers.Factory(
        ReviewService,
        review_repository=repositories.review_repository,
    )

    booking_service = providers.Factory(
        BookingService,
        booking_repository=repositories.booking_repository,
    )


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
        ]
    )

    services = providers.Container(
        ServiceContainer,
    )

    user_use_case = providers.Factory(
        UserUseCase,
        user_service=services.user_service
    )

    hotel_use_case = providers.Factory(
        HotelUseCase,
        hotel_service=services.hotel_service
    )

    room_use_case = providers.Factory(
        RoomUseCase,
        room_service=services.room_service
    )

    auth_use_case = providers.Factory(
        AuthUseCase,
        auth_service=services.auth_service
    )

    review_use_case = providers.Factory(
        ReviewUseCase,
        review_service=services.review_service
    )

    booking_use_case = providers.Factory(
        BookingUseCase,
        booking_service=services.booking_service
    )

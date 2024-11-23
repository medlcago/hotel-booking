from dependency_injector import containers, providers

from core.database import Database
from core.settings import settings
from core.uow import UnitOfWork
from services.auth import AuthService
from services.hotel import HotelService
from services.review import ReviewService
from services.room import RoomService
from services.user import UserService
from use_cases.auth import AuthUseCase
from use_cases.hotel import HotelUseCase
from use_cases.review import ReviewUseCase
from use_cases.room import RoomUseCase
from use_cases.user import UserUseCase


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.auth.auth",
            "api.v1.users.users",
            "api.v1.hotels.hotels",
            "api.v1.rooms.rooms",
            "api.v1.reviews.reviews",
            "api.deps",
        ]
    )

    db = providers.Singleton(
        Database,
        url=settings.db.dsn,
        echo=settings.debug,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
        pool_timeout=settings.db.pool_timeout
    )

    uow = providers.Factory(
        UnitOfWork,
        session=db.provided.session,
    )

    # user
    user_service = providers.Factory(
        UserService,
        uow=uow
    )

    user_use_case = providers.Factory(
        UserUseCase,
        user_service=user_service
    )

    # hotel
    hotel_service = providers.Factory(
        HotelService,
        uow=uow,
    )

    hotel_use_case = providers.Factory(
        HotelUseCase,
        hotel_service=hotel_service
    )

    # room
    room_service = providers.Factory(
        RoomService,
        uow=uow,
    )

    room_use_case = providers.Factory(
        RoomUseCase,
        room_service=room_service
    )

    # auth
    auth_service = providers.Factory(
        AuthService,
        uow=uow,
    )

    auth_use_case = providers.Factory(
        AuthUseCase,
        auth_service=auth_service
    )

    # review
    review_service = providers.Factory(
        ReviewService,
        uow=uow
    )

    review_use_case = providers.Factory(
        ReviewUseCase,
        review_service=review_service
    )

from dependency_injector.wiring import Provide, inject

from core.container import Container
from domain.usecases import IBookingUseCase


@inject
async def cancel_pending_booking(
        booking_id: int,
        user_id: int,
        booking_use_case: IBookingUseCase = Provide[Container.booking_use_case],
) -> None:
    await booking_use_case.cancel_pending_booking(
        booking_id=booking_id,
        user_id=user_id,
    )

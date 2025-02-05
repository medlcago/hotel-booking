from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from api.deps import YookassaWebhookNotification
from core.container import Container
from domain.usecases import IBookingUseCase
from schemas.booking import BookingCancelRequest

router = APIRouter(prefix="/events", tags=["events"])


@router.post(path="/yookassa")
@inject
async def yookassa_events(
        notification_object: YookassaWebhookNotification,
        booking_use_case: IBookingUseCase = Depends(Provide[Container.booking_use_case]),
):
    payment = notification_object.object
    event = notification_object.event
    metadata = payment.metadata

    booking_id = int(metadata["booking_id"])
    user_id = int(metadata["user_id"])
    match event:
        case "payment.waiting_for_capture":
            await booking_use_case.confirm_booking(
                booking_id=booking_id,
                user_id=user_id
            )
        case "payment.canceled":
            await booking_use_case.cancel_booking(
                schema=BookingCancelRequest(
                    booking_id=booking_id,
                ),
                user_id=user_id
            )

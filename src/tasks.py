import platform
import uuid

from asgiref.sync import async_to_sync
from celery import Celery

from core.container import Container
from core.db.scope import session_scope
from core.settings import settings
from utils.booking import cancel_pending_booking
from utils.db_session import init_db_session
from utils.mail import send_email
from utils.template import render_template


def create_celery_app() -> Celery:
    container: Container = Container()
    _db_engine = container.db_engine()
    init_db_session(_db_engine)
    _celery_app = container.celery_app()
    return _celery_app


celery = create_celery_app()


@celery.task(name="send_confirmation_email", ingore_result=True)
def send_confirmation_email(email: str, token: str) -> None:
    confirmation_link = f"{settings.base_url}/confirm-email?token={token}"
    body = render_template("email_confirmation.html", confirmation_link=confirmation_link)
    async_to_sync(send_email)(
        subject="Confirm your email",
        recipients=[email],
        body=body,
        content_type="html"
    )


@celery.task(name="send_reset_password_email", ignore_result=True)
def send_reset_password_email(email: str, token: str) -> None:
    # TODO password reset form
    body = render_template("reset_password.html", token=token)
    async_to_sync(send_email)(
        subject="Reset your password",
        recipients=[email],
        body=body,
        content_type="html"
    )


@celery.task(
    name="cancel_pending_booking",
    autoretry_for=(Exception,),
    retry_backoff=True
)
def cancel_pending_booking_task(booking_id: int) -> None:
    async def async_wrapper():
        session_id = uuid.uuid4()
        async with session_scope(session_id):
            await cancel_pending_booking(
                booking_id=booking_id,
            )

    async_to_sync(async_wrapper)()


if __name__ == "__main__":
    args = ["worker", "--loglevel=INFO"]
    os_name = platform.system()
    if os_name == "Windows":
        args.append("--pool=solo")
    celery.worker_main(argv=args)

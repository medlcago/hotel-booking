import platform
import uuid

from asgiref.sync import async_to_sync
from celery import Celery
from dependency_injector import providers
from sqlalchemy import NullPool

from core.container import Container
from core.db.engine import Engine
from core.db.scope import session_scope
from core.exceptions import BookingNotFound
from core.settings import settings
from utils.booking import cancel_pending_booking
from utils.db_session import init_db_session
from utils.mail import send_email
from utils.template import render_template


def create_celery_app() -> Celery:
    container: Container = Container()
    container.db_engine.override(providers.Singleton(
        Engine.create,
        url=settings.db.dsn,
        poolclass=NullPool
    ))  # poolclass=NullPool - fix InterfaceError - cannot perform operation: another operation is in progress
    _db_engine = container.db_engine()
    init_db_session(_db_engine)
    _celery_app = container.celery_app()
    return _celery_app


celery = create_celery_app()


@celery.task(name="send_confirmation_code", ingore_result=True)
def send_confirmation_code_task(email: str, code: str) -> None:
    body = render_template("email_confirmation.html", code=code)
    async_to_sync(send_email)(
        subject="Confirm your email",
        recipients=[email],
        body=body,
        content_type="html"
    )


@celery.task(name="send_reset_password_code", ignore_result=True)
def send_reset_password_code_task(email: str, code: str) -> None:
    body = render_template("reset_password.html", code=code)
    async_to_sync(send_email)(
        subject="Reset your password",
        recipients=[email],
        body=body,
        content_type="html"
    )


@celery.task(
    name="cancel_pending_booking",
    dont_autoretry_for=(BookingNotFound,),
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": None},
    retry_backoff=True
)
def cancel_pending_booking_task(booking_id: int, user_id: int) -> None:
    async def async_wrapper():
        session_id = str(uuid.uuid4())
        async with session_scope(session_id):
            await cancel_pending_booking(
                booking_id=booking_id,
                user_id=user_id,
            )

    async_to_sync(async_wrapper)()


if __name__ == "__main__":
    args = ["worker", "--loglevel=INFO"]
    os_name = platform.system()
    if os_name == "Windows":
        args.append("--pool=solo")
    celery.worker_main(argv=args)

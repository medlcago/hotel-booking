from asgiref.sync import async_to_sync
from celery import Celery

from core.settings import settings
from utils.mail import send_email
from utils.template import render_template

celery = Celery(
    __name__,
    broker=settings.celery.broker_url,
    backend=settings.celery.backend_url
)
celery.conf.update(
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True
)


@celery.task(name="send_confirmation_email", ingore_result=True)
def send_confirmation_email(email: str, token: str) -> None:
    confirmation_link = f"{settings.base_url}/verify-email?token={token}"
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


if __name__ == "__main__":
    args = ["worker", "--loglevel=INFO"]
    celery.worker_main(argv=args)

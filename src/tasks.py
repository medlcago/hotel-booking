from asgiref.sync import async_to_sync
from celery import Celery

from core.security import create_url_safe_token
from core.settings import settings
from utils.mail import send_email

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
def send_confirmation_email(email: str) -> None:
    token = create_url_safe_token(data=dict(email=email))
    confirmation_link = f"{settings.base_url}/verify-email?token={token}"
    async_to_sync(send_email)(
        subject="Confirm your email",
        recipients=[email],
        body=f"Please click the following link to confirm your email: {confirmation_link}",
        content_type="plain"
    )


if __name__ == "__main__":
    args = ["worker", "--loglevel=INFO"]
    celery.worker_main(argv=args)

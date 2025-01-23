from typing import TypedDict, Unpack

from celery import Celery


class CelerySettings(TypedDict):
    broker_url: str
    backend_url: str
    timezone: str
    enable_utc: bool
    broker_connection_retry_on_startup: bool


def create_celery(**kwargs: Unpack[CelerySettings]) -> Celery:
    celery = Celery(
        __name__,
        broker=kwargs.get("broker_url"),
        backend=kwargs.get("backend_url"),
    )
    celery.conf.update(
        timezone=kwargs.get("timezone"),
        enable_utc=kwargs.get("enable_utc"),
        broker_connection_retry_on_startup=kwargs.get("broker_connection_retry_on_startup"),
    )
    return celery

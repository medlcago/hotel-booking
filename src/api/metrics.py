from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


def init_metrics(app: FastAPI) -> None:
    from prometheus_fastapi_instrumentator import Instrumentator
    Instrumentator().instrument(app).expose(app, tags=["metrics"], response_class=PlainTextResponse)

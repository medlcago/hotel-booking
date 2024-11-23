from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator


def init_metrics(app: FastAPI) -> None:
    Instrumentator().instrument(app).expose(app, tags=["metrics"], response_class=PlainTextResponse)

from fastapi import FastAPI


def init_middlewares(app: FastAPI):
    from .session_context import SessionContextMiddleware
    app.add_middleware(SessionContextMiddleware)  # noqa

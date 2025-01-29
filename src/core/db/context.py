from contextvars import ContextVar, Token


class SessionContext:
    _session_context: ContextVar[str] = ContextVar("session_context")

    @classmethod
    def get_session_context(cls) -> str:
        return cls._session_context.get()

    @classmethod
    def set_session_context(cls, session_id: str) -> Token:
        return cls._session_context.set(session_id)

    @classmethod
    def reset_session_context(cls, token: Token) -> None:
        cls._session_context.reset(token)

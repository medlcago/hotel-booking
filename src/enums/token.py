from enum import StrEnum, auto


class TokenType(StrEnum):
    access = auto()
    refresh = auto()
    nameless = auto()

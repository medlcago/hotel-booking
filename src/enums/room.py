from enum import StrEnum, auto


class RoomType(StrEnum):
    """
    single - одноместный номер
    double - двухместный номер
    suite - люкс
    deluxe - номер повышенной комфортности
    twin - номер с двумя отдельными кроватями
    family - семейный номер
    king - номер с кроватью размера "king-size"
    queen - номер с кроватью размера "queen-size"
    studio - студия
    penthouse - пентхаус
    """
    single = auto()
    double = auto()
    suite = auto()
    deluxe = auto()
    twin = auto()
    family = auto()
    king = auto()
    queen = auto()
    studio = auto()
    penthouse = auto()

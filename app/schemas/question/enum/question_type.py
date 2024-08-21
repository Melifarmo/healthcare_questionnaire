from enum import StrEnum, auto


class QuestionType(StrEnum):
    text = auto()
    numeric = auto()
    options = auto()

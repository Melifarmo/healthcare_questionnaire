from enum import StrEnum, auto


class PatientAnswerType(StrEnum):
    direct = auto()
    option = auto()
    bool = auto()

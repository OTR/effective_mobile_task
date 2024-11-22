from abc import ABC, abstractmethod


class BaseBookException(Exception):
    """
    Базовое кастомное исключение, означающее ошибку на уровне приложения.
    Чтобы отделить такие исключения от исключений интерпретатора Python.
    Все другие, более детальные исключения приложения должны наследоваться от этого класса
    """

class PublishingYearMustBeNumericException(BaseBookException):
    """Исключение для неправильного ввода года публикации"""

    def __init__(self, *args, given_year: str):
        msg = f"Год выпуска должен быть числом. Дано: `{given_year}`"
        super().__init__(*args)

class UnexpectedBookException(BaseBookException):
    """Неизвестное Исключение"""

    def __init__(self, *args):
        super().__init__(*args)

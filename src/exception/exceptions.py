from abc import ABC, abstractmethod


class BaseBookException(Exception):
    """
    Базовое кастомное исключение, означающее ошибку на уровне приложения.
    Чтобы отделить такие исключения от исключений интерпретатора Python.
    Все другие, более детальные исключения приложения должны наследоваться от этого класса
    """

class PublishingYearMustBeNumericException(BaseBookException):
    """Исключение для неправильного ввода года публикации"""

    def __init__(self, given_year: str):
        msg = f"Год выпуска должен быть числом. Дано: `{given_year}`"
        super().__init__(msg)

class UnexpectedBookException(BaseBookException):
    """Неизвестное Исключение"""

    def __init__(self, *args):
        super().__init__(*args)

class IncorrectBookIdException(BaseBookException):
    """Исключения для неправильного ввода ID в консоль"""

    def __init__(self, given_id: str):
        msg = f"Некорректный ID книги. Дано: `{given_id}`"
        super().__init__(msg)

class IncorrectBookStatusException(BaseBookException):
    """Исключение для неправильного ввода статуса книги"""

    def __init__(self, given_status: str):
        msg = f"Некорректный статус для книги. Статус должен быть 'available' или 'borrowed'. Дано: `{given_status}`"
        super().__init__(msg)

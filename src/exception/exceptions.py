class BaseBookError(Exception):
    """
    Базовое кастомное исключение, означающее ошибку на уровне приложения.

    Чтобы отделить такие исключения от исключений интерпретатора Python.
    Все другие, более детальные исключения приложения должны наследоваться от этого класса
    """


class PublishingYearMustBeNumericError(BaseBookError):
    """Исключение для неправильного ввода года публикации."""

    def __init__(self, given_year: str):
        """
        Конструктор.

        Args:
            given_year: переданная строка, которая не является годом выпуска
        """
        msg = f'Год выпуска должен быть числом. Дано: `{given_year}`'
        super().__init__(msg)


class UnexpectedBookError(BaseBookError):
    """Неизвестное Исключение."""


class IncorrectBookIdError(BaseBookError):
    """Исключения для неправильного ввода ID в консоль."""

    def __init__(self, given_id: str):
        """
        Переопределяем конструктор.

        Args:
            given_id: str переданная строка которая не является ID
        """
        msg = f'Некорректный ID книги. Дано: `{given_id}`'
        super().__init__(msg)


class IncorrectBookStatusError(BaseBookError):
    """Исключение для неправильного ввода статуса книги."""

    def __init__(self, given_status: str):
        """
        Переопределяем конструктор.

        Args:
            given_status: str переданный статус
        """
        msg = f"Некорректный статус для книги. Статус должен быть 'available' или 'borrowed'. Дано: `{given_status}`"
        super().__init__(msg)


class BookByIdNotFoundError(BaseBookError):
    """Исключение для ситуации когда не найдена книга в хранилище по ID."""

    def __init__(self, desired_id: int):
        """
        Переопределяем конструктор.

        Args:
            desired_id: ID книги которую запросил пользователь
        """
        msg = f'Не найдена книга с ID: {desired_id}'
        super().__init__(msg)

from dataclasses import dataclass

from src.exception.exceptions import IncorrectBookStatusError


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    _status: str = 'available'

    @property
    def status(self) -> str:
        """
        Геттер для поля status.

        Returns:
            str: статус книги в строковом представлении
        """
        return self._status

    @status.setter
    def status(self, new_status: str) -> None:
        """
        Установить новый status для книги.

        Args:
            new_status: str новый статус книги

        Raises:
            IncorrectBookStatusException: если переданный статус не валидный
        """
        if new_status not in {'available', 'borrowed'}:
            raise IncorrectBookStatusError(new_status)
        self._status = new_status

    def __str__(self) -> str:
        """
        Переопределяем str метод для красивого вывода полей книги.

        Returns:
            str: Строковое представление датакласса
        """
        return (f'ID: {self.id}, Заголовок: {self.title}, Автор: {self.author},'
            f' Год выпуска: {self.year}, Статус: {self.status}')

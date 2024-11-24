from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entity import Book


class BaseBookRepository(ABC):

    @abstractmethod
    def add_book(self, book: Book) -> None:
        """Добавить книгу в репозиторий"""
        pass

    @abstractmethod
    def delete_book_by_id(self, book_id: int) -> None:
        """Удалить книгу из репозитория по ID."""
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Получить книгу из репозитория по ID."""
        pass

    @abstractmethod
    def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None
    ) -> List[Book]:
        """Найти книгу по заголовку, автору, или году издания."""
        pass

    @abstractmethod
    def list_books(self) -> List[Book]:
        """Отобразить все доступные книги"""
        pass

    @abstractmethod
    def update_book(self, book: Book) -> None:
        """Изменить описание книги"""
        pass

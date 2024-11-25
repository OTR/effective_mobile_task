from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entity import Book


class BaseBookRepository(ABC):

    @abstractmethod
    def add_book(self, book: Book) -> None:
        """
        Добавить книгу в репозиторий.

        Args:
            book: Book экземпляр книги для добавления в репозиторий
        """

    @abstractmethod
    def delete_book_by_id(self, book_id: int) -> None:
        """
        Удалить книгу из репозитория по ID.

        Args:
            book_id: int ID книги для удаления
        """

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Получить книгу из репозитория по ID.

        Args:
            book_id: int ID книги для получения

        Returns:
            Optional[Book] возвращает книгу если найдена, или None если нет
        """

    @abstractmethod
    def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[Book]:
        """
        Найти книгу по заголовку, автору, или году издания.

        Args:
            title: Optional[str] заголовок книги для поиска
            author: Optional[str] автор книги для поиска
            year: Optional[int] кон издания книги для поиска

        Returns: List[Book] список книг из репозитория соответствующим поисковому запросу
        """

    @abstractmethod
    def list_books(self) -> List[Book]:
        """
        Отобразить все доступные книги.

        Returns: List[Book] список книг в репозитории
        """

    @abstractmethod
    def update_book(self, book: Book) -> None:
        """
        Изменить описание книги.

        Args:
            book: Book экземпляр новой книги для замещения книги по ID в репозиторий
        """

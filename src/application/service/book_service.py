from typing import List, Optional

from src.domain.entity import Book
from src.domain.repository import BaseBookRepository
from src.exception.exceptions import BookByIdNotFoundException


class BookService:

    def __init__(self, repository: BaseBookRepository):
        """
        Создать сервис библиотеки книг с зависимостью абстрактного репозитория.

        Args:
            repository: BaseBookRepository dependency that stores books in file
        """
        self.repository = repository

    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Добавить книгу в библиотеку.

        Args:
            title: Заголовок
            author: Автор
            year: Год издания

        Returns:
            Book: экземпляр сущности книга
        """
        books: list[Book] = self.repository.list_books()
        new_id: int = self._generate_unique_id(books)

        new_book = Book(id=new_id, title=title, author=author, year=year)
        self.repository.add_book(new_book)
        return new_book

    def delete_book_by_id(self, book_id: int) -> None:
        """
        Удалить книгу по ID.

        Args:
             book_id: ID книги

        Raises:
            BookByIdNotFoundException: если не найдено книги с указанным ID
        """
        if not self.repository.get_book_by_id(book_id):
            raise BookByIdNotFoundException(desired_id=book_id)
        self.repository.delete_book_by_id(book_id)

    def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[Book]:
        """
        Найти книгу по заголовку, автору или году издания.

        Args:
            title: Заголовок
            author: автор
            year: год издания

        Returns:
            list[Book]: Список книг подходящих под поисковый критерий или пустой список если нет совпадений.
        """
        return self.repository.search_books(title=title, author=author, year=year)

    def list_books(self) -> List[Book]:
        """
        Отобразить все книги существующие в библиотеке.

        Returns:
            list[Book]: Список всех книг
        """
        return self.repository.list_books()

    def set_book_status(self, book_id: int, new_status: str) -> None:
        """
        Изменить статус книги.

        Args:
            book_id: ID книги
            new_status: новый статус для книги, доступные значения "available" или "borrowed"

        Raises:
            BookByIdNotFoundException: если не найдено книги с указанным ID
        """
        book = self.repository.get_book_by_id(book_id)
        if not book:
            raise BookByIdNotFoundException(desired_id=book_id)

        book.set_status(new_status)
        self.repository.update_book(book)

    @staticmethod
    def _generate_unique_id(books: list[Book]) -> int:
        """
        Сгенерировать новый уникальный ID на основе уже существующих книг в репозитории.

        Args:
            books: list[Book] коллекция уже существующих книг

        Returns:
            int: новый свободный уникальный ID для книги
        """
        return max((book.id for book in books), default=0) + 1

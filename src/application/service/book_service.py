from typing import List, Optional

from src.domain.entity import Book
from src.domain.repository import BaseBookRepository


class BookService:

    def __init__(self, repository: BaseBookRepository):
        """
        Создать сервис библиотеки книг с зависимостью абстрактного репозитория
        """
        self.repository = repository

    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Добавить книгу в библиотеку.

        :param title: Заголовок
        :param author: Автор
        :param year: Год издания
        :return: экземпляр сущности книга
        """
        books: list[Book] = self.repository.list_books()
        new_id: int = BookService._generate_unique_id(books)

        new_book = Book(id=new_id, title=title, author=author, year=year)
        self.repository.add_book(new_book)
        return new_book

    @staticmethod
    def _generate_unique_id(books: list[Book]) -> int:
        """Сгенерировать новый уникальный ID на основе уже существующих книг в репозитории"""
        new_id = max((book.id for book in books), default=0) + 1
        return new_id

    def delete_book_by_id(self, book_id: int) -> None:
        """
        Удалить книгу по ID.

        :param book_id: ID книги
        """
        if not self.repository.get_book_by_id(book_id):
            raise ValueError(f"Не найдена книга с ID: {book_id}")
        self.repository.delete_book_by_id(book_id)

    def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None
    ) -> List[Book]:
        """
        Найти книгу по заголовку, автору или году издания.

        :param title: Заголовок
        :param author: автор
        :param year: год издания
        :return: Список книг подходящих под поисковый критерий или пустой список если нет совпадений.
        """
        return self.repository.search_books(title=title, author=author, year=year)

    def list_books(self) -> List[Book]:
        """
        Отобразить все книги существующие в библиотеке

        :return: Список всех книг
        """
        return self.repository.list_books()

    def change_book_status(self, book_id: int, new_status: str) -> None:
        """
        Изменить статус книги

        :param book_id: ID книги
        :param new_status: новый статус для книги, доступные значения "available" или "borrowed"
        """
        book = self.repository.get_book_by_id(book_id)
        if not book:
            raise ValueError(f"Не найдено книги с ID: {book_id}")

        book.change_status(new_status)
        self.repository.update_book(book)

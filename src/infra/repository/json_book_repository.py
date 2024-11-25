import json
import os
from copy import deepcopy
from typing import List, Optional

from src.domain.entity import Book
from src.domain.repository import BaseBookRepository


class JsonBookRepository(BaseBookRepository):
    _DEFAULT_INDENT: int = 4

    def __init__(self, file_path: str):
        """
        Создать репозиторий, хранящий книги в JSON файлах.

        Args:
            file_path: str путь к JSON файлу для хранения книг
        """
        self.file_path: str = file_path
        self._ensure_file_exists()
        self.books: list[Book] = self._read_books()

    def add_book(self, book: Book) -> None:
        """
        Добавить книгу в хранилище.

        Args:
            book: Book сущность Book для сохранения в JSON файл
        """
        self.books.append(book)
        self._write_books(self.books)

    def delete_book_by_id(self, book_id: int) -> None:
        """
        Удалить книгу из хранилища по ID.

        Args:
            book_id: int ID книги для удаления
        """
        self.books = [book for book in self.books if book.id != book_id]
        self._write_books(self.books)

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Получить книгу из JSON файла по ID.

        Args:
            book_id: int ID книги для удаления

        Returns:
            Optional[Book] найденная книга по ID или None если не найдена
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[Book]:
        """
        Найти книги в JSON файле по заданному критерию поиска.

        Искомое слово содержится в заголовке книге,
        либо искомое слово содержится в авторе книги либо год эквивалентен указанному

        Args:
            title: Optional[str] Заголовок
            author: Optional[str] Автор
            year: Optional[int] Год издания

        Returns:
            list[Book]: список книг подпадающих под поисковый критерий
        """
        result: list[Book] = deepcopy(self.books)
        if title:
            result = [book for book in result if title.lower() in book.title.lower()]
        if author:
            result = [book for book in result if author.lower() in book.author.lower()]
        if year:
            result = [book for book in result if book.year == year]
        return result

    def list_books(self) -> List[Book]:
        """
        Загрузить все имеющиеся в JSON файле книги.

        Returns:
            list[Book]: список книг или пустой список
        """
        return self.books

    def update_book(self, book: Book) -> None:
        """
        Обновить сущность Book в JSON хранилище книг.

        Args:
            book: Book сущность Book
        """
        for index, existing_book in enumerate(self.books):
            if existing_book.id == book.id:
                self.books[index] = book
                break
        self._write_books(self.books)

    def _write_books(self, books: List[Book]) -> None:
        """
        Сохранить все книги в JSON файл.

        Args:
            books: list[Book] список сущностей Book
        """
        with open(self.file_path, 'w') as file1:
            json.dump([book.__dict__ for book in books], file1, indent=self._DEFAULT_INDENT)

    def _ensure_file_exists(self) -> None:
        """Проверить существует ли файл по заданному пути, если нет - то создать пустой JSON файл."""
        try:
            with open(self.file_path, 'w') as file1:
                json.dump([], file1)
        except FileExistsError:
            pass  # noqa: WPS420

    def _read_books(self) -> List[Book]:
        """
        Извлечь все книги из JSON файла.

        Returns:
            list[Book]: список сущностей Book или пустой список
        """
        with open(self.file_path, 'r') as file1:
            storage_data: list[dict] = json.load(file1)
        return [Book(**book_item) for book_item in storage_data]

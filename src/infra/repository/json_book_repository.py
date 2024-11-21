import json
from typing import List, Optional

from src.domain.entity import Book
from src.domain.repository import BaseBookRepository


class JsonBookRepository(BaseBookRepository):
    _DEFAULT_INDENT: int = 4

    def __init__(self, file_path: str):
        """
        Создать репозиторий, хранящий книги в JSON файлах
        :param file_path: путь к JSON файлу для хранения книг
        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Проверить существует ли файл по заданному пути, если нет - то создать пустой JSON файл.
        """
        try:
            with open(self.file_path, "w") as file1:
                json.dump([], file1)
        except FileExistsError:
            pass

    def _read_books(self) -> List[Book]:
        """
        Извлечь все книги из JSON файла
        :return: список сущностей Book или пустой список
        """
        with open(self.file_path, "r") as file1:
            data = json.load(file1)
        return [Book(**item) for item in data]

    def _write_books(self, books: List[Book]) -> None:
        """
        Сохранить все книги в JSON файл
        :param books: список сущностей Book
        """
        with open(self.file_path, "w") as file1:
            json.dump([book.__dict__ for book in books], file1, indent=self._DEFAULT_INDENT)

    def add_book(self, book: Book) -> None:
        """
        :param book: сущность Book для сохранения в JSON файл
        """
        books = self._read_books()
        books.append(book)
        self._write_books(books)

    def delete_book_by_id(self, book_id: int) -> None:
        """
        :param book_id: ID книги для удаления
        """
        books = self._read_books()
        books = [book for book in books if book.id != book_id]
        self._write_books(books)

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Получить книгу из JSON файла по ID
        :param book_id: ID книги для удаления
        """
        books = self._read_books()
        for book in books:
            if book.id == book_id:
                return book
        return None

    def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None
    ) -> List[Book]:
        """
        Найти книги в JSON файле по заданному критерию поиска

        :param title:
        :param author:
        :param year:
        :return:
        """
        books = self._read_books()
        result = books
        if title:
            result = [book for book in result if title.lower() in book.title.lower()]
        if author:
            result = [book for book in result if author.lower() in book.author.lower()]
        if year:
            result = [book for book in result if book.year == year]
        return result

    def list_books(self) -> List[Book]:
        """
        Загрузить все имеющиеся в JSON файле книги
        :return: список книг или пустой список
        """
        return self._read_books()

    def update_book(self, book: Book) -> None:
        """
        Обновить сущность Book в JSON хранилище книг
        :param book: сущность Book
        """
        books = self._read_books()
        for i, existing_book in enumerate(books):
            if existing_book.id == book.id:
                books[i] = book
                break
        self._write_books(books)

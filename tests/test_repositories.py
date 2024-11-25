import json
import unittest
from tempfile import NamedTemporaryFile
from src.domain.entity import Book
from src.domain.repository import BaseBookRepository
from src.infra.repository import JsonBookRepository


class TestJsonBookRepository(unittest.TestCase):

    def setUp(self) -> None:
        """Создаем временный файл для хранилища книг"""
        self.temp_file = NamedTemporaryFile(delete=False, mode='w')
        self.temp_file.write(json.dumps([]))
        self.temp_file.close()
        self.repository: BaseBookRepository = JsonBookRepository(self.temp_file.name)

    def tearDown(self) -> None:
        """Закрываем и удаляем временный файл"""
        self.temp_file.close()

    def test_add_and_list_books(self) -> None:
        """
        Позитивный тест-кейс: После добавления книги в репозиторий в нем содержится только одна книга
        Дано: Создаем валидную книгу
        Ожидаемый результат: В хранилище содержится ровно одна книга с заданным заголовком
        """
        book = Book(id=1, title="Заголовок", author="Автор", year=2023)
        self.repository.add_book(book)
        books = self.repository.list_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Заголовок")

    def test_delete_book(self) -> None:
        """
        Позитивный тест-кейс: Удаление книги из репозитория по ID
        Дано: Создаем валидную книгу
        Ожидаемый результат: В хранилище пусто
        """
        book: Book = Book(id=1, title="Заголовок", author="Автор", year=2023)
        self.repository.add_book(book)
        self.repository.delete_book_by_id(1)
        books: list[Book] = self.repository.list_books()
        self.assertEqual(len(books), 0)

    def test_get_book_by_id(self) -> None:
        """
        Позитивный тест-кейс: Получение книги из репозитория по ID
        Дано: Создаем валидную книгу
        Ожидаемый результат: В хранилище находится книга с заданным заголовком
        """
        book: Book = Book(id=1, title="Заголовок", author="Автор", year=2023)
        self.repository.add_book(book)
        found_book: Book = self.repository.get_book_by_id(1)
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.title, "Заголовок")

    def test_search_books(self) -> None:
        """
        Позитивный тест-кейс: Поиск по хранилищу по точному соответствию заголовка
        Дано: Создаем две валидные книги
        Ожидаемый результат: В хранилище находится ровно одна книга с требуемым заголовком
        """
        self.repository.add_book(Book(id=1, title="Заголовок 1", author="Автор", year=2023))
        self.repository.add_book(Book(id=2, title="Заголовок 2", author="Автор", year=2022))
        results: list[Book] = self.repository.search_books(title="Заголовок 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Заголовок 1")

    def test_update_book(self) -> None:
        """
        Позитивный тест-кейс: После обновления книги, в хранилище появляется книга с новым заголовком
        Дано: Книга с валидным заголовком
        Ожидаемый результат: В хранилище содержится книга с новым заголовком
        """
        book: Book = Book(id=1, title="Заголовок", author="Автор", year=2023)
        self.repository.add_book(book)
        book.title = "Новый заголовок"
        self.repository.update_book(book)
        updated_book: Book = self.repository.get_book_by_id(1)
        self.assertEqual(updated_book.title, "Новый заголовок")


if __name__ == "__main__":
    unittest.main()

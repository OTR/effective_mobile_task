import unittest
from tempfile import NamedTemporaryFile

from src.application.service import BookService
from src.domain.entity import Book
from src.domain.repository import BaseBookRepository
from src.infra.repository import JsonBookRepository


class TestBookService(unittest.TestCase):

    def setUp(self):
        """
        Подготовить временный файл для хранения книг на диске.
        Инициализировать необходимые зависимости
        """
        self.temp_file = NamedTemporaryFile(delete=False)
        self.repository: BaseBookRepository = JsonBookRepository(self.temp_file.name)
        self.service = BookService(self.repository)

    def tearDown(self):
        """Закрыть и удалить временный файл"""
        self.temp_file.close()

    def test_add_book(self) -> None:
        """
        Позитивный тест-кейс: Добавить книгу в хранилище
        Дано: валидные поля для книги
        Ожидаемый результат: сущность книги создается успешно
        """
        book: Book = self.service.add_book("Заголовок", "Автор", 2023)
        self.assertEqual(book.title, "Заголовок")
        self.assertEqual(book.author, "Автор")
        self.assertEqual(book.year, 2023)
        self.assertEqual(book.status, "available")

    def test_delete_book(self) -> None:
        """
        Позитивный тест-кейс: Удаление книги по ID из хранилища
        Дано: Валидная книга добавлена в хранилище
        Ожидаемый результат: Попытка получить книгу из хранилища возвращает None
        """
        book: Book = self.service.add_book("Заголовок", "Автор", 2022)
        self.service.delete_book_by_id(book.id)
        self.assertIsNone(self.repository.get_book_by_id(book.id))

    def test_search_books(self):
        """
        Позитивный тест-кейс: Книга добавленная в хранилище успешно находится по заголовку
        Дано: Валидная книга добавлена в хранилище
        Ожидаемый результат: Поиск по хранилищу возвращает ровно одну книгу
        """
        self.service.add_book("Заголовок", "Автор", 2021)
        results: list[Book] = self.service.search_books(title="Заголовок")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Заголовок")

    def test_list_books(self):
        """
        Позитивный тест-кейс: Добавление двух книг в хранилище пополняет хранилище
        Дано: добавляем две валидных книги
        Ожидаемый результат: в хранилище ровно 2 книги
        """
        self.service.add_book("Заголовок 1", "Автор 1", 2020)
        self.service.add_book("Заголовок 2", "Автор 2", 2019)
        books: list[Book] = self.service.list_books()
        self.assertEqual(len(books), 2)

    def test_change_book_status(self):
        """
        Позитивный тест-кейс: Установка нового статуса меняет статус
        Дано: Книга со статусом "доступно"
        Ожидаемый результат: Книга со статусом "взята"
        """
        book: Book = self.service.add_book("Заголовок", "Автор", 2017)
        self.assertEqual(book.status, "available")
        self.service.set_book_status(book.id, "borrowed")
        updated_book: Book = self.repository.get_book_by_id(book.id)
        self.assertEqual(updated_book.status, "borrowed")


if __name__ == "__main__":
    unittest.main()

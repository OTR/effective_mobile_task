import sys
from doctest import UnexpectedException
from pathlib import Path
from typing import Optional

from src.application.service import BookService
from src.domain.entity import Book
from src.domain.repository import BaseBookRepository
from src.exception.exceptions import PublishingYearMustBeNumericException
from src.infra.repository import JsonBookRepository
from src.infra.view import BookView

class CliAdapter:

    @staticmethod
    def main():
        """
        Главный цикл консольного приложения библиотеки книг
        """
        project_root: Path = Path(__file__).parent.parent.parent.parent
        file_path: str = str(project_root / '.data' / 'books.json')
        repository: BaseBookRepository = JsonBookRepository(file_path=file_path)
        service = BookService(repository)

        while True:
            BookView.get_menu()
            option: str = input("Введите пункт из меню: ").strip()

            if option == "1":
                title: str = input("Введите заголовок книги: ").strip()
                author: str = input("Введите автора книги: ").strip()
                try:
                    input_year: str = input("Введите год выпуска: ").strip()
                    year: int = int(input_year)
                except ValueError as err:
                    if len(err.args) > 0 and str(err.args[0]).startswith("invalid literal for int() with base 10:"):
                        raise PublishingYearMustBeNumericException(given_year=input_year)
                    else:
                        raise UnexpectedBookException(err)
                    continue

                book: Book = service.add_book(title, author, year)
                print(f"Книга успешно добавлена, присвоен ID: {book.id}")

            elif option == "2":
                try:
                    book_id: int = int(input("Введите ID книги для удаления: ").strip())
                    service.delete_book_by_id(book_id)
                    print("Книга успешно удалена")
                except ValueError:
                    print("Некорректный ID, попробуйте ещё раз")
                except Exception as e:
                    print(e)

            elif option == "3":
                title: str = input("Введите заголовок книги для поиска (или нажмите Enter чтобы пропустить): ").strip()
                author: str = input("Введите автора книги для поиска (или нажмите Enter чтобы пропустить): ").strip()
                year: str = input("Введите год выпуска для поиска (или нажмите Enter чтобы пропустить): ").strip()
                try:
                    year: Optional[int] = int(year) if year else None
                except ValueError:
                    print("Год выпуска должен быть числом. Попробуйте ещё раз")
                    continue

                books: list[Book] = service.search_books(title, author, year)
                if books:
                    print("\n--- Результат поиска ---")
                    for book in books:
                        print(book)
                else:
                    print("Не найдено книг в хранилище по указанному поисковому запросу")

            elif option == "4":
                books: list[Book] = service.list_books()
                if books:
                    print("\n--- Доступные книги ---")
                    for book in books:
                        print(book)
                else:
                    print("К сожалению в хранилище нет книг")

            elif option == "5":
                try:
                    book_id: int = int(input("Введите ID книги для обновления: ").strip())
                    new_status: str = input("Введите новый статус, доступные значения: available, borrowed: ").strip().lower()
                    service.set_book_status(book_id, new_status)
                    print("Статус книги успешно обновлен")
                except ValueError:
                    print("Неправильный ввод. Попробуйте ещё раз")
                except Exception as e:
                    print(e)

            elif option == "6":
                print("Спасибо, что посетили нашу библиотеку!")
                sys.exit()

            else:
                print("Некорректный ввод пункта. Выберите число от 1 до 6 включительно.")


if __name__ == "__main__":
    CliAdapter.main()

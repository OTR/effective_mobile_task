import sys
from pathlib import Path
from typing import Optional

from src.application.service import BookService
from src.domain.entity import Book
from src.domain.repository import BaseBookRepository
from src.exception import PublishingYearMustBeNumericError, UnexpectedBookError
from src.exception.exceptions import IncorrectBookIdError, BaseBookError
from src.infra.adapter.menu_option import MenuOption
from src.infra.config.string_constants import *
from src.infra.repository import JsonBookRepository


class CliAdapter:

    def __init__(self):
        """Инициализация зависимостей"""
        project_root: Path = Path(__file__).parent.parent.parent.parent
        file_path: str = str(project_root / '.data' / 'books.json')
        repository: BaseBookRepository = JsonBookRepository(file_path=file_path)
        self.service = BookService(repository)

    def main(self) -> None:
        """Главный цикл консольного приложения библиотеки книг"""
        while True:
            print("_" * 80)
            print(BOOK_MENU)
            try:
                option: str = input(INPUT_MENU_OPTION).strip()
                match MenuOption(option):
                    case MenuOption.ADD_BOOK:
                        self._handle_add_book()
                    case MenuOption.DELETE_BOOK:
                        self._handle_delete_book()
                    case MenuOption.SEARCH_BOOK:
                        self._handle_search_books()
                    case MenuOption.LIST_BOOKS:
                        self._handle_list_books()
                    case MenuOption.SET_STATUS:
                        self._handle_set_status()
                    case MenuOption.EXIT:
                        CliAdapter._handle_exit()
                        break
                    case _:
                        CliAdapter._handle_invalid_option()
            except KeyboardInterrupt:
                print(EXIT_OPTION_MESSAGE)
                break
            except BaseBookError as err:
                print(err)
                print(TRY_AGAIN_MESSAGE)
                continue
            except ValueError as err:
                if EMPTY_MAIN_MENU_INPUT in str(err):
                    print(INCORRECT_MAIN_MENU_OPTION_MESSAGE + " " + EMPTY_MAIN_MENU_MESSAGE)
                    continue
                else:
                    print(INCORRECT_MAIN_MENU_OPTION_MESSAGE + " " + str(err))
                    continue
            except Exception as err:
                print(UNEXPECTED_ERROR_HAPPENED + str(err))
                sys.exit(1)

    def _handle_add_book(self) -> None:
        """Обработка пункта меню: 1. Добавить книгу"""
        title: str = input(INPUT_BOOK_TITLE).strip()
        author: str = input(INPUT_BOOK_AUTHOR).strip()
        input_year: str = EMPTY_STRING
        try:
            input_year = input(INPUT_PUBLISHING_YEAR).strip()
            year: int = int(input_year)
        except ValueError as err:
            if NUMBER_FORMAT_EXCEPTION in str(err):
                raise PublishingYearMustBeNumericError(given_year=input_year)
            else:
                raise UnexpectedBookError(err)

        book: Book = self.service.add_book(title, author, year)
        print(BOOK_SUCCESSFULLY_ADDED + str(book.id))

    def _handle_delete_book(self) -> None:
        """Обработка пункта меню: 2. Удалить книгу"""
        input_book_id: str = EMPTY_STRING
        try:
            input_book_id = input(INPUT_ID_FOR_DELETION).strip()
            book_id: int = int(input_book_id)
            self.service.delete_book_by_id(book_id)
            print(BOOK_SUCCESSFULLY_DELETED)
        except ValueError as err:
            if NUMBER_FORMAT_EXCEPTION in str(err):
                raise IncorrectBookIdError(given_id=input_book_id)
            else:
                raise UnexpectedBookError(err)

    def _handle_search_books(self) -> None:
        """Обработка пункта меню: 3. Найти книгу"""
        title: str = input(INPUT_TITLE_OR_SKIP).strip()
        author: str = input(INPUT_AUTHOR_OR_SKIP).strip()
        input_year: str = input(INPUT_PUBLISHING_YEAR_OR_SKIP).strip()
        try:
            year: Optional[int] = int(input_year) if input_year else EMPTY_STRING
        except ValueError as err:
            if NUMBER_FORMAT_EXCEPTION in str(err):
                raise PublishingYearMustBeNumericError(given_year=input_year)
            else:
                raise UnexpectedBookError(err)

        books: list[Book] = self.service.search_books(title, author, year)
        if books:
            print(SEARCH_RESULT_TITLE)
            for book in books:
                print(book)
        else:
            print(NO_BOOKS_FOUND_MESSAGE)

    def _handle_list_books(self) -> None:
        """Обработка пункта меню: 4. Отобразить все книги"""
        books: list[Book] = self.service.list_books()
        if books:
            print(LOOKUP_RESULT_TITLE)
            for book in books:
                print(book)
        else:
            print(NO_BOOKS_FOUND_MESSAGE)

    def _handle_set_status(self) -> None:
        """"Обработка пункта меню: 5. Изменить статус книги"""
        input_book_id: str = EMPTY_STRING
        try:
            input_book_id = input(INPUT_ID_FOR_UPDATE).strip()
            book_id: int = int(input_book_id)
            new_status: str = input(INPUT_NEW_BOOK_STATUS).strip().lower()
            self.service.set_book_status(book_id, new_status)
            print(STATUS_SUCCESSFULLY_UPDATED)
        except ValueError as err:
            if NUMBER_FORMAT_EXCEPTION in str(err):
                raise IncorrectBookIdError(given_id=input_book_id)
            else:
                raise UnexpectedBookError(err)

    @staticmethod
    def _handle_exit():
        """Обработка опции `Выход` в меню"""
        print(EXIT_OPTION_MESSAGE)
        sys.exit()

    @staticmethod
    def _handle_invalid_option():
        """Обработка некорректного ввода пункта меню"""
        print(INCORRECT_MAIN_MENU_OPTION_MESSAGE)

from enum import Enum


class MenuOption(Enum):
    """Пункты консольного меню в виде констант"""
    ADD_BOOK = "1"
    DELETE_BOOK = "2"
    SEARCH_BOOK = "3"
    LIST_BOOKS = "4"
    SET_STATUS = "5"
    EXIT = "6"

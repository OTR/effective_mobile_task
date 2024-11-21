from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    status: str = "available"

    def change_status(self, new_status: str) -> None:
        if new_status not in {"available", "borrowed"}:
            raise ValueError("Статус должен быть 'available' или 'borrowed'.")
        self.status = new_status

    def __str__(self) -> str:
        """Переопределяем str метод для красивого вывода полей книги."""
        return  (f"ID: {self.id}, Заголовок: {self.title}, Автор: {self.author},"
                 f" Год выпуска: {self.year}, Статус: {self.status}")

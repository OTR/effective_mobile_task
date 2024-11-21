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

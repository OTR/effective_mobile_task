from pathlib import Path

from src.application.service import BookService
from src.domain.repository import BaseBookRepository
from src.infra.adapter import CliAdapter
from src.infra.repository import JsonBookRepository


def main():
    project_root: Path = Path(__file__).parent
    file_path: str = str(project_root / '.data' / 'books.json')
    repository: BaseBookRepository = JsonBookRepository(file_path=file_path)
    book_service: BookService = BookService(repository)
    adapter: CliAdapter = CliAdapter(book_service)
    adapter.main()

if __name__ == '__main__':
    main()

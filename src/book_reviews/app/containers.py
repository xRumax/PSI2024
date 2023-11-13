from dependency_injector import containers, providers
from dotenv import load_dotenv
from app.db import Database
from .book.repositories import BookRepository
from .book.services import BookService
from .author.repositories import AuthorRepository
from .author.services import AuthorService

load_dotenv()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".book.routes", ".author.routes"]
    )
    config = providers.Configuration()
    config.db.url.from_env("DATABASE_URL")
    db = providers.Singleton(Database, db_url=config.db.url)

    book_repository = providers.Factory(
        BookRepository, session_factory=db.provided.session
    )

    book_service = providers.Factory(
        BookService,
        book_repository=book_repository,
    )
    author_repository = providers.Factory(
        AuthorRepository, session_factory=db.provided.session
    )
    author_service = providers.Factory(
        AuthorService,
        author_repository=author_repository,
    )

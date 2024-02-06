from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class CreateGenre:
    def __init__(self, repository: GenreRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        is_active: bool = True
        categories: set[UUID] = field(default_factory=set)

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        # Application Business Rule: Categories devem existir para criar um Genre
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - category_ids}")

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories=input.categories,
            )
        except ValueError as err:
            raise InvalidGenre(err)

        self.repository.save(genre)
        return self.Output(id=genre.id)

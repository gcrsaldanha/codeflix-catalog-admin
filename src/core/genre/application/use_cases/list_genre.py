from dataclasses import dataclass
from uuid import UUID

from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    categories: set[UUID]
    is_active: bool


class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[GenreOutput]

    def execute(self, input: Input) -> Output:
        genres = self.repository.list()

        data = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                categories=genre.categories,
                is_active=genre.is_active,
            )
            for genre in genres
        ]

        return self.Output(data=data)

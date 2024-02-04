from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestDeleteGenre:
    def test_delete_genre_from_repository(self):
        genre = Genre(name="Drama")
        genre_repository = InMemoryGenreRepository()
        genre_repository.save(genre)
        use_case = DeleteGenre(repository=genre_repository)

        assert genre_repository.get_by_id(genre.id) == genre
        use_case.execute(DeleteGenre.Input(id=genre.id))
        assert genre_repository.get_by_id(genre.id) is None

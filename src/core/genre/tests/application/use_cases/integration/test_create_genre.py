import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestCreateGenre:
    def test_create_genre_with_associated_categories(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        category_repository.save(Category(name="Category 1", description="Category 1 description"))
        category_repository.save(Category(name="Category 2", description="Category 2 description"))

        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )
        output = use_case.execute(
            CreateGenre.Input(
                name="Genre 1",
                categories={cat.id for cat in category_repository.list()},
            )
        )

        assert len(genre_repository.list()) == 1
        created_genre = genre_repository.get_by_id(output.id)
        assert created_genre.name == "Genre 1"
        assert created_genre.categories == {cat.id for cat in category_repository.list()}
        assert created_genre.is_active

    def test_create_genre_with_inexistent_categories_raise_an_error(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )

        with pytest.raises(RelatedCategoriesNotFound, match="Categories with provided IDs not found: ") as exc:
            use_case.execute(
                CreateGenre.Input(
                    name="Genre 1",
                    categories={uuid.uuid4()}
                )
            )

        assert len(genre_repository.list()) == 0

    def test_create_genre_without_categories(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )

        output = use_case.execute(
            CreateGenre.Input(
                name="Genre 1",
            )
        )

        assert len(genre_repository.list()) == 1
        created_genre = genre_repository.get_by_id(output.id)
        assert created_genre.name == "Genre 1"
        assert created_genre.categories == set()
        assert created_genre.is_active

import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TestCreateGenre:
    def test_when_provided_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
        mock_empty_category_repository,
        mock_genre_repository,
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_empty_category_repository,
        )

        with pytest.raises(RelatedCategoriesNotFound, match="Categories with provided IDs not found: ") as exc:
            category_id = uuid.uuid4()
            use_case.execute(CreateGenre.Input(
                name="Genre 1",
                categories={category_id},
            ))

        assert str(category_id) in str(exc.value)

    def test_when_created_genre_is_invalid_then_raise_invalid_genre(
        self,
        documentary_category,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ) -> None:
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        # InvalidGenre (application), not ValueError (domain)
        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(CreateGenre.Input(
                name="",
                categories={documentary_category.id, movie_category.id},
            ))

    def test_when_created_genre_is_valid_and_categories_exist_then_save_genre(
        self,
        documentary_category,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        output = use_case.execute(CreateGenre.Input(
            name="Romance",
            categories={documentary_category.id, movie_category.id},
        ))

        assert output == CreateGenre.Output(id=output.id)
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Romance",
                is_active=True,
                categories={documentary_category.id, movie_category.id},
            )
        )

    def test_create_genre_without_categories(
        self,
        mock_genre_repository,
        mock_category_repository_with_categories,
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        output = use_case.execute(CreateGenre.Input(
            name="Romance",
        ))

        assert output == CreateGenre.Output(id=output.id)
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Romance",
                is_active=True,
                categories=set(),
            )
        )

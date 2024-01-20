from unittest.mock import create_autospec

import pytest
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
)
from src.core.category.domain.category import Category


class TestListCategory:
    @pytest.fixture
    def category_movie(self) -> Category:
        return Category(
            name="Filme",
            description="Categoria de filmes",
        )

    @pytest.fixture
    def category_series(self) -> Category:
        return Category(
            name="Séries",
            description="Categoria de séries",
        )

    @pytest.fixture
    def mock_empty_repository(self) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = []
        return repository

    @pytest.fixture
    def mock_populated_repository(
        self,
        category_movie: Category,
        category_series: Category,
    ) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = [
            category_movie,
            category_series,
        ]
        return repository

    def test_when_no_categories_then_return_empty_list(
        self,
        mock_empty_repository: CategoryRepository,
    ) -> None:
        use_case = ListCategory(repository=mock_empty_repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListCategoryResponse(data=[])

    def test_when_categories_exist_then_return_mapped_list(
        self,
        mock_populated_repository: CategoryRepository,
        category_movie: Category,
        category_series: Category,
    ) -> None:
        use_case = ListCategory(repository=mock_populated_repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active,
                ),
                CategoryOutput(
                    id=category_series.id,
                    name=category_series.name,
                    description=category_series.description,
                    is_active=category_series.is_active,
                ),
            ]
        )

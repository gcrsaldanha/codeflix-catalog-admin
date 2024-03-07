from unittest.mock import create_autospec

import pytest

from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse, ListOutputMeta,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


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
    def category_documentary(self) -> Category:
        return Category(
            name="Documentário",
            description="Categoria de documentários",
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
        category_documentary: Category,
    ) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = [
            category_movie,
            category_series,
            category_documentary,  # Fora de "ordem" - Application que ordena
        ]
        return repository

    def test_when_no_categories_then_return_empty_list(
        self,
        mock_empty_repository: CategoryRepository,
    ) -> None:
        use_case = ListCategory(repository=mock_empty_repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListCategoryResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=0,
            ),
        )

    def test_when_categories_exist_then_return_mapped_list(
        self,
        mock_populated_repository: CategoryRepository,
        category_movie: Category,
        category_series: Category,
        category_documentary: Category,
    ) -> None:
        use_case = ListCategory(repository=mock_populated_repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_documentary.id,
                    name=category_documentary.name,
                    description=category_documentary.description,
                    is_active=category_documentary.is_active,
                ),
                CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active,
                ),
                # Documentary vem antes, "empurra" o Movie para fora da página
                # Por isso precisamos ordernar a lista de categorias antes de paginar
                # CategoryOutput(
                #     id=category_series.id,
                #     name=category_series.name,
                #     description=category_series.description,
                #     is_active=category_series.is_active,
                # ),
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=3,
            ),
        )

    def test_fetch_page_without_elements(self, mock_populated_repository: CategoryRepository) -> None:
        use_case = ListCategory(repository=mock_populated_repository)
        response = use_case.execute(request=ListCategoryRequest(current_page=3))

        assert response == ListCategoryResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=3,
                per_page=2,
                total=3,
            ),
        )

    def test_fetch_last_page_with_elements(
        self,
        mock_populated_repository: CategoryRepository,
        category_series: Category,  # Foi "empurrado" para última página
    ) -> None:
        use_case = ListCategory(repository=mock_populated_repository)
        response = use_case.execute(request=ListCategoryRequest(current_page=2))

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_series.id,
                    name=category_series.name,
                    description=category_series.description,
                    is_active=category_series.is_active,
                )
            ],
            meta=ListOutputMeta(
                current_page=2,
                per_page=2,
                total=3,
            ),
        )

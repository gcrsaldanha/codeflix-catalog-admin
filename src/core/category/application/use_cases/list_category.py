from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListCategoryRequest:
    order_by: str = "name"  # Desafio: ordenação decrescente? ASC/DESC


@dataclass
class ListCategoryResponse:
    data: list[CategoryOutput]


class ListCategory:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.list()

        return ListCategoryResponse(
            data=sorted(
                [
                    CategoryOutput(
                        id=category.id,
                        name=category.name,
                        description=category.description,
                        is_active=category.is_active,
                    ) for category in categories
                ],
                key=lambda category: getattr(category, request.order_by),
            )
        )

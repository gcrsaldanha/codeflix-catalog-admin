from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.exceptions import InvalidCategoryData

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CreateCategoryResponse:
    id: UUID


class CreateCategory:
    def __init__(self, repository: InMemoryCategoryRepository):
        self.repository = repository

    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        try:
            category = Category(
                name=request.name,
                description=request.description,
                is_active=request.is_active,
            )
        except ValueError as err:
            raise InvalidCategoryData(err)

        self.repository.save(category)
        return category.id


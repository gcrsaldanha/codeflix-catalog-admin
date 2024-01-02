from uuid import UUID
from src.core.category.application.use_cases.exceptions import InvalidCategory
from src.core.category.domain.category import Category


class InMemoryCategoryRepository:
    def __init__(self, categories: list[Category] = None) -> None:
        self._categories = categories or []

    def save(self, category: Category):
        self._categories.append(category)


def create_category(name, description, is_active = True, repository = None) -> UUID:
    repository = repository or InMemoryCategoryRepository()

    try:
        category = Category(name=name, description=description, is_active=is_active)
    except ValueError as error:
        raise InvalidCategory(error)

    repository.save(category)
    return category.id

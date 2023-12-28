from uuid import UUID
from src.core.category.domain.category import Category


# input: name, description, is_active
# output: category_id (UUID)
def create_category(name, description, is_active = True) -> UUID:
    category = Category(name=name, description=description, is_active=is_active)
    # TODO: persist category
    return category.id  # Do not return entity

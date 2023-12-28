from uuid import UUID
from unittest.mock import MagicMock
from src.core.category.application.use_cases.create_category import create_category


class TestCreateCategory:
    def test_create_active_category_with_name_and_description(self):
        output = create_category("Movies", "Movie category", is_active=True)
        assert isinstance(output, UUID)

    def test_create_inactive_category_with_name_and_description(self):
        output = create_category("Movies", "Movie category", is_active=False)
        assert isinstance(output, UUID)

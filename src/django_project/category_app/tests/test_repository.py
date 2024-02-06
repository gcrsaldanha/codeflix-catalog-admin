import pytest
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.models import Category as CategoryORM
from src.core.category.domain.category import Category


@pytest.mark.django_db
class TestSave:
    def test_saves_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryORM.objects.count() == 0
        repository.save(category)
        assert CategoryORM.objects.count() == 1
        saved_category = CategoryORM.objects.get()

        assert saved_category.id == category.id
        assert saved_category.name == category.name
        assert saved_category.description == category.description
        assert saved_category.is_active == category.is_active

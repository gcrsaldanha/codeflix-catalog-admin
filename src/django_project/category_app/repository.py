from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category
from src.django_project.category_app.models import Category as CategoryORM


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, model: CategoryORM | None = None):
        self.model = model or CategoryORM

    def save(self, category: Category) -> None:
        category_model = CategoryModelMapper.to_model(category)
        category_model.save()
        # self.model.objects.create(
        #     id=category.id,
        #     name=category.name,
        #     description=category.description,
        #     is_active=category.is_active,
        # )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_model = self.model.objects.get(id=id)
            return CategoryModelMapper.to_entity(category_model)
            # return Category(
            #     id=category_model.id,
            #     name=category_model.name,
            #     description=category_model.description,
            #     is_active=category_model.is_active,
            # )
        except self.model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def list(self) -> list[Category]:
        # return [
        #     Category(
        #         id=category.id,
        #         name=category.name,
        #         description=category.description,
        #         is_active=category.is_active,
        #     ) for category in self.model.objects.all()
        # ]
        return [CategoryModelMapper.to_entity(category) for category in self.model.objects.all()]

    def update(self, category: Category) -> None:
        self.model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )


class CategoryModelMapper:
    @staticmethod
    def to_entity(model: CategoryORM) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
        )

    @staticmethod
    def to_model(entity: Category) -> CategoryORM:
        return CategoryORM(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
        )

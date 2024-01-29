from django.http import QueryDict
from src.django_project.category_app.serializers import CreateCategoryRequestSerializer


class TestCreateCategoryRequestSerializer:
    def test_when_fields_are_valid(self):
        serializer = CreateCategoryRequestSerializer(
            data={
                "name": "Filme",
                "description": "Categoria para filmes",
            }
        )

        assert serializer.is_valid() is True

    def test_when_is_active_is_not_provided_and_partial_then_do_not_add_it_to_serializer(self):
        serializer = CreateCategoryRequestSerializer(
            data={
                "name": "Filme",
                "description": "Categoria para filmes",
            },
            partial=True,
        )

        assert serializer.is_valid() is True
        assert "is_active" not in serializer.validated_data

    def test_when_is_active_is_not_provided_and_not_partial_then_set_to_true(self):
        serializer = CreateCategoryRequestSerializer(
            data={
                "name": "Filme",
                "description": "Categoria para filmes",
            },
        )
        assert serializer.is_valid() is True

        assert serializer.validated_data["is_active"] is True

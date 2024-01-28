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
        is_valid = serializer.is_valid()

        assert is_valid is True

    def test_when_is_active_is_not_provided_then_do_not_add_it_to_serializer(self):
        serializer = CreateCategoryRequestSerializer(
            data={
                "name": "Filme",
                "description": "Categoria para filmes",
            }
        )
        serializer.is_valid()

        assert "is_active" not in serializer.validated_data

    def test_when_is_active_not_provided_but_called_with_query_dict_then_include_it(self):
        data = QueryDict(mutable=True)
        data.update({
            "name": "Filme",
            "description": "Categoria para filmes",
        })

        serializer = CreateCategoryRequestSerializer(data=data)
        serializer.is_valid()

        assert "is_active" in serializer.validated_data
        assert serializer.validated_data["is_active"] is False


    def test_when_called_with_query_dict_but_partial_then_do_not_include_is_active(self):
        data = QueryDict(mutable=True)
        data.update({
            "name": "Filme",
            "description": "Categoria para filmes",
        })

        serializer = CreateCategoryRequestSerializer(data=data, partial=True)
        serializer.is_valid()

        assert "is_active" not in serializer.validated_data

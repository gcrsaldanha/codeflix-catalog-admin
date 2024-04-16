from unittest.mock import patch
from uuid import UUID, uuid4
from django.test import override_settings
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from src.config import DEFAULT_PAGINATION_SIZE
from src.core.category.domain.category import Category

from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.views import CategoryViewSet


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
@patch.object(CategoryViewSet, "permission_classes", [])
class TestListAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/categories/"
        # TODO: Desafio: Obter esse token dinamicamente
        token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJxNm9HUjlpRDZhM3BwWEpxZmoxUW94U0pnZ0lZVmtOUmRnSGJvbHkzX0JrIn0.eyJleHAiOjE3MTMxNTE3MDgsImlhdCI6MTcxMzE1MTQwOCwianRpIjoiYzExYTY5MWEtYjBmNi00Y2ZmLWEzN2QtMTI0MWFmZTgyYWUyIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9jb2RlZmxpeCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIyZTFlMDU5ZS04YjJhLTQwOWMtYWYxOS0xY2U0ZmQzNDJiZGMiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJjb2RlZmxpeC1mcm9udGVuZCIsInNlc3Npb25fc3RhdGUiOiIzZWNlZDIxYi0xN2Q5LTQyMGItODljNS0zMjllMDlmOTY2MGYiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1jb2RlZmxpeCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6IjNlY2VkMjFiLTE3ZDktNDIwYi04OWM1LTMyOWUwOWY5NjYwZiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiYWRtaW4gYWRtaW4iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbiIsImdpdmVuX25hbWUiOiJhZG1pbiIsImZhbWlseV9uYW1lIjoiYWRtaW4iLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSJ9.fSO0GFO2ONhbS2wObskymMNH8EblDidAV7KdX1M7E4d9e0Ot6EKti3npETXnwd8iJYIqoyswX2WAkfhJgW7Ryk5yuomoqmeX1sQEUd9SIzhmX5VUivSUe3TcXCG-RptVwuR9vSXiXlwlOHj-5wy7G5j4UUdNofG07oKTl5_WBvu7XxrBUuH0fGD-NfJV6UMJgeqmZSsNeYDqoY0DHR6jyh1BqSYoQkw1ReczF--YOzCPPwxxjkLGU_l99ibESsAfE_U3cnWVEdvtaOShyoTvJ8Qr19iJgIxvXMughMhs4X8BXYGdeI-MZR6xaBRyCgGLDgoq0ZuQHcS6PtiWx1IRKw"
        response = APIClient(headers={
            "Authorization": f"Bearer {token}",
        }).get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_documentary.id),
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": True,
                },
                {
                    "id": str(category_movie.id),
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                },
            ],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGINATION_SIZE,
                "total": 2,
            },
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@patch.object(CategoryViewSet, "permission_classes", [])
@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_category_with_id_exists_then_return_category(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "data": {
                "id": str(category_movie.id),
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
            }
        }

    def test_when_category_with_id_does_not_exist_then_return_404(
        self,
    ) -> None:
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = f"/api/categories/invalid_id/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}


@patch.object(CategoryViewSet, "permission_classes", [])
@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_category(
        self,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url = reverse("category-list")
        data = {
            "name": "Movie",
            "description": "Movie description",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]

        saved_category = category_repository.get_by_id(response.data["id"])
        assert saved_category == Category(
            id=UUID(response.data["id"]),
            name="Movie",
            description="Movie description",
            is_active=True,
        )

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = reverse("category-list")
        data = {
            "name": "",
            "description": "Movie description",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}


@patch.object(CategoryViewSet, "permission_classes", [])
@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_category(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = reverse("category-detail", kwargs={"pk": category_movie.id})
        data = {
            "name": "Not Movie",
            "description": "Another description",
            "is_active": False,
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category.name == "Not Movie"
        assert updated_category.description == "Another description"
        assert updated_category.is_active is False

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = reverse("category-detail", kwargs={"pk": "invalid-uuid"})
        data = {
            "name": "",
            "description": "Movie description",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
        }

    def test_when_category_with_id_does_not_exist_then_return_404(
        self,
    ) -> None:
        url = reverse("category-detail", kwargs={"pk": uuid4()})
        data = {
            "name": "Not Movie",
            "description": "Another description",
            "is_active": False,
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@patch.object(CategoryViewSet, "permission_classes", [])
@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_category_pk_is_invalid_then_return_400(self) -> None:
        url = reverse("category-detail", kwargs={"pk": "invalid-uuid"})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}

    def test_when_category_not_found_then_return_404(self) -> None:
        url = reverse("category-detail", kwargs={"pk": uuid4()})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_found_then_delete_category(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = reverse("category-detail", kwargs={"pk": category_movie.id})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        assert category_repository.get_by_id(category_movie.id) is None


@patch.object(CategoryViewSet, "permission_classes", [])
@pytest.mark.django_db
class TestPartialUpdateAPI:
    @pytest.mark.parametrize(
        "payload,expected_category_dict",
        [
            (
                {
                    "name": "Not Movie",
                },
                {
                    "name": "Not Movie",
                    "description": "Movie description",
                    "is_active": True,
                },
            ),
            (
                {
                    "description": "Another description",
                },
                {
                    "name": "Movie",
                    "description": "Another description",
                    "is_active": True,
                },
            ),
            (
                {
                    "is_active": False,
                },
                {
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": False,
                },
            ),
        ],
    )
    def test_when_request_data_is_valid_then_update_category(
        self,
        payload: dict,
        expected_category_dict: dict,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = reverse("category-detail", kwargs={"pk": category_movie.id})
        response = APIClient().patch(url, data=payload)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == expected_category_dict["name"]
        assert updated_category.description == expected_category_dict["description"]
        assert updated_category.is_active == expected_category_dict["is_active"]

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = reverse("category-detail", kwargs={"pk": "invalid-uuid"})
        data = {
            "name": "",
            "description": "Movie description",
        }
        response = APIClient().patch(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
        }

    def test_when_category_with_id_does_not_exist_then_return_404(
        self,
    ) -> None:
        url = reverse("category-detail", kwargs={"pk": uuid4()})
        data = {
            "name": "Not Movie",
            "description": "Another description",
            "is_active": False,
        }
        response = APIClient().patch(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

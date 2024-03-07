from uuid import UUID, uuid4
from django.test import override_settings
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def actor():
    return CastMember(
        name="John Doe",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def director():
    return CastMember(
        name="John Krasinski",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_cast_members(
        self,
        actor: CastMember,
        director: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(actor)
        cast_member_repository.save(director)

        url = "/api/cast_members/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(actor.id),
                    "name": "John Doe",
                    "type": "ACTOR",
                },
                {
                    "id": str(director.id),
                    "name": "John Krasinski",
                    "type": "DIRECTOR",
                },
            ]
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        url = reverse("cast_member-list")
        data = {
            "name": "John Doe",
            "type": "ACTOR",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]

        saved_cast_member = cast_member_repository.get_by_id(response.data["id"])
        assert saved_cast_member == CastMember(
            id=UUID(response.data["id"]),
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = reverse("cast_member-list")
        data = {
            "name": "",
            "type": "",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "type": ['"" is not a valid choice.'],
        }


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_cast_member(
        self,
        actor: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(actor)

        url = reverse("cast_member-detail", kwargs={"pk": actor.id})
        data = {
            "name": "Another Actor",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        updated_cast_member = cast_member_repository.get_by_id(actor.id)
        assert updated_cast_member.name == "Another Actor"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = reverse("cast_member-detail", kwargs={"pk": "invalid-uuid"})
        data = {
            "name": "",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "type": ["This field is required."],
        }

    def test_when_cast_member_with_id_does_not_exist_then_return_404(
        self,
    ) -> None:
        url = reverse("cast_member-detail", kwargs={"pk": uuid4()})
        data = {
            "name": "Not Actor",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_cast_member_pk_is_invalid_then_return_400(self) -> None:
        url = reverse("cast_member-detail", kwargs={"pk": "invalid-uuid"})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}

    def test_when_cast_member_not_found_then_return_404(self) -> None:
        url = reverse("cast_member-detail", kwargs={"pk": uuid4()})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_cast_member_found_then_delete_cast_member(
        self,
        actor: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(actor)

        url = reverse("cast_member-detail", kwargs={"pk": actor.id})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        assert cast_member_repository.get_by_id(actor.id) is None

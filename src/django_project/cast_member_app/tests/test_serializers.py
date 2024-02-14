from django.http import QueryDict
from src.core.cast_member.domain.cast_member import CastMemberType
from src.django_project.cast_member_app.serializers import CreateCastMemberRequestSerializer


class TestCreateCastMemberRequestSerializer:
    def test_when_fields_are_valid(self):
        serializer = CreateCastMemberRequestSerializer(
            data={
                "name": "John Doe",
                "type": CastMemberType.ACTOR,
            }
        )

        assert serializer.is_valid() is True

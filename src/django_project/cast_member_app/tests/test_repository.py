import pytest
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


@pytest.mark.django_db
class TestSave:
    def test_saves_cast_member_in_database(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        repository = DjangoORMCastMemberRepository()

        assert CastMemberORM.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberORM.objects.count() == 1
        saved_cast_member = CastMemberORM.objects.get()

        assert saved_cast_member.id == cast_member.id
        assert saved_cast_member.name == cast_member.name
        assert saved_cast_member.type == cast_member.type

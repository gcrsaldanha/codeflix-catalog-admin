import uuid
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestSave:
    def test_can_save_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        repository.save(cast_member)

        assert len(repository.cast_members) == 1
        assert repository.cast_members[0] == cast_member


class TestGetById:
    def test_can_get_cast_member_by_id(self):
        actor = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        director = CastMember(
            name="John Krasinski",
            type=CastMemberType.DIRECTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[
                actor,
                director,
            ]
        )

        cast_member = repository.get_by_id(actor.id)

        assert cast_member == actor

    def test_when_cast_member_does_not_exists_should_return_none(self):
        actor = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[
                actor,
            ]
        )

        cast_member = repository.get_by_id(uuid.uuid4())

        assert cast_member is None


class TestDelete:
    def test_delete_cast_member(self):
        actor = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        director = CastMember(
            name="John Krasinski",
            type=CastMemberType.DIRECTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[
                actor,
                director,
            ]
        )

        repository.delete(actor.id)

        assert len(repository.cast_members) == 1
        assert repository.cast_members[0] == director


class TestUpdate:
    def test_update_cast_member(self):
        actor = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        director = CastMember(
            name="John Krasinski",
            type=CastMemberType.DIRECTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[
                actor,
                director,
            ]
        )

        actor.name = "John Doeee"
        actor.type = CastMemberType.DIRECTOR
        repository.update(actor)

        assert len(repository.cast_members) == 2
        updated_cast_member = repository.get_by_id(actor.id)
        assert updated_cast_member.name == "John Doeee"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_update_non_existent_cast_member_does_not_raise_exception(self):
        repository = InMemoryCastMemberRepository(cast_members=[])

        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        repository.update(cast_member)

        assert len(repository.cast_members) == 0

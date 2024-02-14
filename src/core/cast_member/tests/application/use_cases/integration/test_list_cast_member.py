from unittest.mock import create_autospec

import pytest
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
    ListCastMemberRequest,
    ListCastMemberResponse,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestListCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

    @pytest.fixture
    def director(self) -> CastMember:
        return CastMember(
            name="John Krasinski",
            type=CastMemberType.DIRECTOR,
        )

    def test_when_no_cast_members_then_return_empty_list(self) -> None:
        empty_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(repository=empty_repository)
        response = use_case.execute(request=ListCastMemberRequest())

        assert response == ListCastMemberResponse(data=[])

    def test_when_cast_members_exist_then_return_mapped_list(
        self,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        repository = InMemoryCastMemberRepository()
        repository.save(cast_member=actor)
        repository.save(cast_member=director)

        use_case = ListCastMember(repository=repository)
        response = use_case.execute(request=ListCastMemberRequest())

        assert response == ListCastMemberResponse(
            data=[
                CastMemberOutput(
                    id=actor.id,
                    name=actor.name,
                    type=actor.type,
                ),
                CastMemberOutput(
                    id=director.id,
                    name=director.name,
                    type=director.type,
                ),
            ]
        )

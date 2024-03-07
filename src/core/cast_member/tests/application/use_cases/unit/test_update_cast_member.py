from unittest.mock import create_autospec
import uuid

import pytest
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
    UpdateCastMemberRequest,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestUpdateCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

    @pytest.fixture
    def mock_repository(self, actor: CastMember) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository, instance=True)
        repository.get_by_id.return_value = actor
        return repository

    def test_update_cast_member_name_and_type(
        self,
        mock_repository: CastMemberRepository,
        actor: CastMember,
    ):
        use_case = UpdateCastMember(mock_repository)
        use_case.execute(
            UpdateCastMemberRequest(
                id=actor.id,
                name="John Krasinski",
                type=CastMemberType.DIRECTOR,
            )
        )

        assert actor.name == "John Krasinski"
        assert actor.type == CastMemberType.DIRECTOR
        mock_repository.update.assert_called_once_with(actor)

    def test_when_cast_member_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCastMember(mock_repository)
        request = UpdateCastMemberRequest(
            id=uuid.uuid4(),
            name="John Krasinski",
            type=CastMemberType.DIRECTOR,
        )

        with pytest.raises(CastMemberNotFound) as exc:
            use_case.execute(request)

        mock_repository.update.assert_not_called()
        assert str(exc.value) == f"CastMember with {request.id} not found"

    def test_when_cast_member_is_updated_to_invalid_state_then_raise_exception(
        self,
        mock_repository: CastMemberRepository,
        actor: CastMember,
    ) -> None:
        use_case = UpdateCastMember(mock_repository)
        request = UpdateCastMemberRequest(
            id=actor.id,
            name="",
            type="",
        )

        with pytest.raises(InvalidCastMember) as exc:
            use_case.execute(request)

        mock_repository.update.assert_not_called()
        assert str(exc.value) == "name cannot be empty"

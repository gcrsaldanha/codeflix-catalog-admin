from unittest.mock import create_autospec
import uuid

import pytest
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = DeleteCastMember(mock_repository)
        use_case.execute(DeleteCastMemberRequest(id=cast_member.id))

        mock_repository.delete.assert_called_once_with(cast_member.id)


    def test_when_cast_member_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCastMember(mock_repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteCastMemberRequest(id=uuid.uuid4()))

        mock_repository.delete.assert_not_called()

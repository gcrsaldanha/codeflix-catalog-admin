
from dataclasses import dataclass
from uuid import UUID
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember

@dataclass
class UpdateCastMemberRequest:
    id: UUID
    name: str
    type: CastMemberType


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, request: UpdateCastMemberRequest) -> None:
        cast_member = self.repository.get_by_id(request.id)
        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with {request.id} not found")

        try:
            cast_member.update_cast_member(
                name=request.name,
                type=request.type,
            )
        except ValueError as error:
            raise InvalidCastMember(error)

        self.repository.update(cast_member)


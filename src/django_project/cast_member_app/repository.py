from uuid import UUID
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, model: CastMemberORM | None = None):
        self.model = model or CastMemberORM

    def save(self, cast_member: CastMember) -> None:
        self.model.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member_model = self.model.objects.get(id=id)
            return CastMember(
                id=cast_member_model.id,
                name=cast_member_model.name,
                type=CastMemberType(cast_member_model.type),
            )
        except self.model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def list(self) -> list[CastMember]:
        return [
            CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=CastMemberType(cast_member.type),  # convert str => StrEnum
            ) for cast_member in self.model.objects.all()
        ]

    def update(self, cast_member: CastMember) -> None:
        self.model.objects.filter(pk=cast_member.id).update(
            name=cast_member.name,
            type=cast_member.type,
        )

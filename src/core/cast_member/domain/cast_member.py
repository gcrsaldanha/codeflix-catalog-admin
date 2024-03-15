from dataclasses import dataclass, field
from enum import StrEnum
import uuid
from uuid import UUID

from src.core._shared.domain.entity import Entity


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass(eq=False)
class CastMember(Entity):
    name: str
    type: CastMemberType

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")

        if not self.name:
            raise ValueError("name cannot be empty")

        if not self.type in CastMemberType:
            raise ValueError("type must be a valid CastMemberType: actor or director")

    def __str__(self):
        return f"{self.name} - {self.type}"

    def __repr__(self):
        return f"<CastMember {self.name} {self.type} ({self.id})>"

    def update_cast_member(self, name, type):
        self.name = name
        self.type = type

        self.validate()

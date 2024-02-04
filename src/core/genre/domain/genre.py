from dataclasses import dataclass, field
import uuid
from typing import Set
from uuid import UUID


@dataclass
class Genre:
    name: str
    is_active: bool = True
    categories: Set[UUID] = field(default_factory=set)
    id: UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")

        if not self.name:
            raise ValueError("name cannot be empty")

    def __str__(self):
        return f"{self.name} (active: {self.is_active})"

    def __repr__(self):
        return f"<Genre {self.name} ({self.id})>"

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False

        return self.id == other.id

    def add_category(self, category_id: UUID) -> None:
        self.categories.add(category_id)

    def remove_category(self, category_id: UUID) -> None:
        self.categories.remove(category_id)

    def change_name(self, name):
        self.name = name
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID

from src.core._shared.domain.notification import Notification


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid.uuid4)
    notification: Notification = field(default_factory=Notification, init=False)

    def __eq__(self, other: "Entity") -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id

    @abstractmethod
    def validate(self):
        pass

from abc import ABC
from dataclasses import dataclass, field
from typing import Dict


@dataclass(slots=True, frozen=True)
class DomainEvent(ABC):
    payload: Dict = field(default_factory=dict)

    @property
    def type(self) -> str:
        return self.__class__.__name__


class EventServiceInterface(ABC):
    def send(self, event: DomainEvent) -> None:
        raise NotImplementedError


class EventService(EventServiceInterface):
    def send(self, event: DomainEvent) -> None:
        print("Sending event", event)

from abc import ABC, abstractmethod

from src.core._shared.domain.events.domain_event import DomainEvent


class EventDispatcher(ABC):
    @abstractmethod
    def dispatch(self, event: DomainEvent) -> None:
        pass

    @abstractmethod
    def serialize(self, event: DomainEvent) -> bytes:
        pass

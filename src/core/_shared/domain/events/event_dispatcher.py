from abc import ABC, abstractmethod

from src.core._shared.domain.events.event import Event


class EventDispatcher(ABC):
    @abstractmethod
    def dispatch(self, event: Event) -> None:
        pass

    @abstractmethod
    def serialize(self, event: Event) -> bytes:
        pass

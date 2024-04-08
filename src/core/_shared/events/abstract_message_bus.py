from abc import ABC, abstractmethod

from src.core._shared.events.event import Event


class AbstractMessageBus(ABC):
    @abstractmethod
    def handle(self, events: list[Event]) -> None:
        pass

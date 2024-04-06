from abc import ABC, abstractmethod

from src.core._shared.domain.events.event import Event


class AbstractMessageBus(ABC):
    @abstractmethod
    def dispatch(self, events: list[Event]) -> None:
        pass

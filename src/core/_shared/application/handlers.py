from abc import ABC, abstractmethod
from typing import Generic

from src.core._shared.domain.events.event import TEvent


class Handler(ABC, Generic[TEvent]):
    @abstractmethod
    def handle(self, event: TEvent) -> None:
        pass

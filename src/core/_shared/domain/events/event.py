from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import TypeVar



@dataclass(frozen=True, kw_only=True)
class Event(ABC):
    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def payload(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        return f"{self.type}: {self.payload}"

    def __repr__(self) -> str:
        return self.__str__()

    @abstractmethod
    def serialize(self) -> str:
        pass


TEvent = TypeVar('TEvent', bound=Event)

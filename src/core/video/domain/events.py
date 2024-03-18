from dataclasses import dataclass

from src.core._shared.domain.event import DomainEvent


@dataclass(frozen=True, slots=True)
class AudioVideoMediaUpdated(DomainEvent):
    pass

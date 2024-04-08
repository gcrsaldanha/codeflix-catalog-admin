from dataclasses import dataclass

from src.core._shared.events.event import Event


@dataclass(frozen=True)
class AudioVideoMediaUpdatedIntegrationEvent(Event):
    resource_id: str
    file_path: str

import json
from dataclasses import dataclass

from src.core._shared.domain.events.event import Event


@dataclass(frozen=True)
class AudioVideoMediaUpdatedIntegrationEvent(Event):
    resource_id: str
    file_path: str

    def serialize(self) -> str:
        return json.dumps(self.payload)

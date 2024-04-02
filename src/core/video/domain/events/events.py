import json
from dataclasses import dataclass
from uuid import UUID

from src.core._shared.domain.events.domain_event import DomainEvent
from src.core.video.domain.value_objects import MediaType


@dataclass(frozen=True)
class AudioVideoMediaUpdated(DomainEvent):
    aggregate_id: UUID
    media_type: MediaType
    file_path: str

    def serialize(self) -> str:
        payload = {
            "resource_id": f"{str(self.aggregate_id)}.{self.media_type}",
            "file_path": self.file_path,
        }
        return json.dumps(payload)

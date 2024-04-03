from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from src.core._shared.infrastructure.storage.abstract_storage import AbstractStorage
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus
from src.core.video.domain.video_repository import VideoRepository


class UploadVideo:
    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str

    def __init__(self, repository: VideoRepository, storage_service: AbstractStorage) -> None:
        self.repository = repository
        self.storage_service = storage_service

    def execute(self, input: Input) -> None:
        # TODO: trailer vs video
        video = self.repository.get_by_id(input.video_id)
        if video is None:
            raise VideoNotFound(input.video_id)

        file_path = Path("videos") / str(video.id) / input.file_name
        self.storage_service.store(file_path, input.content, input.content_type)
        video_media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING,
        )
        video.update_video_media(video_media)

        self.repository.update(video)

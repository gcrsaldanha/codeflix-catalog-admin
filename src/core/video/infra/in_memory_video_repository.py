from uuid import UUID
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video


class InMemoryVideoRepository(VideoRepository):
    def __init__(self, videos: list[Video] = None):
        self.videos: list[Video] = videos or []

    def save(self, video: Video) -> None:
        self.videos.append(video)

    def get_by_id(self, id: UUID) -> Video | None:
        return next(
            (video for video in self.videos if video.id == id), None
        )

    def delete(self, id: UUID) -> None:
        video = self.get_by_id(id)
        if video:
            self.videos.remove(video)

    def list(self) -> list[Video]:
        return [video for video in self.videos]

    def update(self, video: Video) -> None:
        old_video = self.get_by_id(video.id)
        if old_video:
            self.videos.remove(old_video)
            self.videos.append(video)

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.video.domain.video import Video


class VideoRepository(ABC):
    @abstractmethod
    def save(self, video: Video):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Video | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Video]:
        raise NotImplementedError

    @abstractmethod
    def update(self, video: Video) -> None:
        raise NotImplementedError

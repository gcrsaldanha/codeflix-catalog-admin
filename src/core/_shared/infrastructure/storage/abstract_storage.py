from abc import ABC, abstractmethod
from mimetypes import MimeTypes
from pathlib import Path


class AbstractStorage(ABC):
    @abstractmethod
    def store(self, file_path: Path, content: bytes, content_type: str = "") -> str:
        pass

    @abstractmethod
    def retrieve(self, file_path: Path) -> bytes:
        pass

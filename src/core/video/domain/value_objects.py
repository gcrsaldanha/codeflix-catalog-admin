import enum
from dataclasses import dataclass
from enum import Enum, auto, unique
from uuid import UUID


@unique
class Rating(Enum):
    ER = auto()
    L = auto()
    AGE_10 = auto()
    AGE_12 = auto()
    AGE_14 = auto()
    AGE_16 = auto()
    AGE_18 = auto()


@unique
class MediaStatus(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()


@dataclass(frozen=True)
class ImageMedia:
    name: str
    raw_location: str


@dataclass(frozen=True)
class AudioVideoMedia:
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus

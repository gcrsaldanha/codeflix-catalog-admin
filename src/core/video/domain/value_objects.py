"""
- Value Objects
    - Rating: ENUM (ER, L, AGE_10, AGE_12, AGE_14, AGE_16, AGE_18)
    - ImageMedia:
        - Id: UUID | String
        - CheckSum: String
        - Name: String
        - Location: String
    - AudioVideoMedia
        - Id: UUID | String
        - CheckSum: String
        - Name: String
        - RawLocation: String
        - EncondedLocation: String
        - Status: MediaStatus: ENUM (PENDING, PROCESSING, COMPLETED, ERROR)
"""

from dataclasses import dataclass
from enum import Enum, auto, unique
from uuid import UUID


@unique
class MediaStatus(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()


@unique
class Rating(Enum):
    ER = auto()
    L = auto()
    AGE_10 = auto()
    AGE_12 = auto()
    AGE_14 = auto()
    AGE_16 = auto()
    AGE_18 = auto()


@dataclass(frozen=True)
class ImageMedia:
    id: UUID
    check_sum: str
    name: str
    location: str


@dataclass(frozen=True)
class AudioVideoMedia:
    id: UUID
    check_sum: str
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus

from dataclasses import dataclass
from decimal import Decimal
from typing import Set
from uuid import UUID

from src.core._shared.domain.entity import Entity
from src.core.video.domain.events import AudioVideoMediaUpdated
from src.core.video.domain.value_objects import Rating, ImageMedia, AudioVideoMedia


@dataclass(slots=True)
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: Rating

    categories: Set[UUID]
    genres: Set[UUID]
    cast_members: Set[UUID]

    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None

    def __post_init__(self):
        self.validate()

    def update(
        self,
        title: str,
        description: str,
        launch_year: int,
        duration: Decimal,
        published: bool,
        rating: Rating,
        categories: Set[UUID],
        genres: Set[UUID],
        cast_members: Set[UUID],
    ) -> None:
        # TODO: Implementar métodos "de negócio": set_title, set_description, publish, rate, etc.
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.rating = rating
        self.categories = categories
        self.genres = genres
        self.cast_members = cast_members
        self.validate()

    def validate(self):
        # TODO: Usar pydantic para validar os tipos dos atributos
        # TODO: Validações específicas: title, description
        if not self.title:
            self.notification.add_error("Title is required")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)


    def update_banner(self, banner: ImageMedia) -> None:
        self.banner = banner
        self.validate()

    def update_thumbnail(self, thumbnail: ImageMedia) -> None:
        self.thumbnail = thumbnail
        self.validate()

    def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
        self.thumbnail_half = thumbnail_half
        self.validate()

    def update_video_media(self, video: AudioVideoMedia) -> None:
        self.video = video
        self.validate()

    def update_trailer(self, trailer: AudioVideoMedia) -> None:
        self.trailer = trailer
        self.validate()

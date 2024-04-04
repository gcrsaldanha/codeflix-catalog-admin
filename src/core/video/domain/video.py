from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from src.core._shared.domain.entity import Entity
from src.core.video.domain.events.events import AudioVideoMediaUpdated
from src.core.video.domain.value_objects import Rating, ImageMedia, AudioVideoMedia, MediaStatus, MediaType


@dataclass(slots=True, kw_only=True)
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    opened: bool
    published: bool

    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]

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
        rating: Rating,
        categories: set[UUID],
        genres: set[UUID],
        cast_members: set[UUID],
    ) -> None:
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.rating = rating
        self.categories = categories
        self.genres = genres
        self.cast_members = cast_members
        self.validate()

    def publish(self) -> None:
        if not self.video:
            self.notification.add_error("Video media is required to publish the video")
        elif self.video.status != MediaStatus.COMPLETED:
            self.notification.add_error("Video must be fully processed to be published")

        self.published = True
        self.validate()

    def validate(self):
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
        self.events.append(AudioVideoMediaUpdated(
            aggregate_id=self.id,
            file_path=video.raw_location,
            media_type=MediaType.VIDEO,
        ))

    def update_trailer(self, trailer: AudioVideoMedia) -> None:
        self.trailer = trailer
        self.validate()

    def process(self, status: MediaStatus, encoded_location: str = "") -> None:
        if status == MediaStatus.COMPLETED:
            self.video = self.video.complete(encoded_location)
            self.publish()
        else:
            self.video = self.video.fail()

        self.validate()

from dataclasses import dataclass
from decimal import Decimal
from typing import Set
from uuid import UUID

from src.core._shared.domain.notification import Notification
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.use_cases.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class CreateVideoWithoutMedia:
    @dataclass
    class Input:
        title: str
        description: str
        launch_year: int
        opened: bool
        duration: Decimal
        rating: Rating
        categories: Set[UUID]
        genres: Set[UUID]
        cast_members: Set[UUID]

    @dataclass
    class Output:
        id: UUID

    def __init__(
        self,
        video_repository: VideoRepository,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ):
        self._video_repository = video_repository
        self._category_repository = category_repository
        self._genre_repository = genre_repository
        self._cast_member_repository = cast_member_repository

    def execute(self, request: Input) -> Output:
        notification = Notification()
        notification.add_errors(self.validate_categories(request.categories))
        notification.add_errors(self.validate_genres(request.genres))
        notification.add_errors(self.validate_cast_members(request.cast_members))

        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)

        try:
            video = Video(
                title=request.title,
                description=request.description,
                launch_year=request.launch_year,
                opened=request.opened,
                duration=request.duration,
                rating=request.rating,
                categories=request.categories,
                genres=request.genres,
                cast_members=request.cast_members,
            )
        except ValueError as err:
            raise InvalidVideo(err)

        self._video_repository.save(video)

        return self.Output(id=video.id)

    def validate_categories(self, category_ids: Set[UUID]) -> list[str]:
        existing_category_ids = {category.id for category in self._category_repository.list()}
        if not category_ids.issubset(existing_category_ids):
            return ["Invalid categories"]

    def validate_genres(self, genre_ids: Set[UUID]) -> list[str]:
        existing_genre_ids = {genre.id for genre in self._genre_repository.list()}
        if not genre_ids.issubset(existing_genre_ids):
            return ["Invalid genres"]

    def validate_cast_members(self, cast_member_ids: Set[UUID]) -> list[str]:
        existing_cast_member_ids = {cast_member.id for cast_member in self._cast_member_repository.list()}
        if not cast_member_ids.issubset(existing_cast_member_ids):
            return ["Invalid cast members"]

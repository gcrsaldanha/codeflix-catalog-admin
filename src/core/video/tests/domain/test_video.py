from uuid import uuid4
from decimal import Decimal

import pytest

from src.core.video.domain.events import AudioVideoMediaUpdated
from src.core.video.domain.value_objects import Rating, ImageMedia, AudioVideoMedia, MediaStatus, MediaType
from src.core.video.domain.video import Video


@pytest.fixture
def video() -> Video:
    return Video(
        title="Sample Video",
        description="A test video",
        launch_year=2022,
        duration=Decimal("120.5"),
        rating=Rating.AGE_12,
        categories={uuid4()},
        genres={uuid4()},
        cast_members={uuid4()},
        opened=True,
    )


class TestVideoEntity:
    def test_valid_video(self, video: Video) -> None:
        video.validate()
        assert video.notification.has_errors is False

    def test_invalid_video(self, video: Video) -> None:
        video.title = ""
        with pytest.raises(ValueError, match="Title is required"):
            video.validate()

    def test_optional_attributes(self):
        # Create a Video object with optional attributes
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            opened=True,
            categories={uuid4()},
            genres={uuid4()},
            cast_members={uuid4()},
            banner=ImageMedia("banner.jpg", "path/to/banner"),
            thumbnail=None,  # Testing None value for an optional attribute
            trailer=AudioVideoMedia("trailer.mp4", "raw_path", "encoded_path", MediaStatus.COMPLETED, media_type=MediaType.TRAILER),
        )
        assert video.notification.has_errors is False


class TestPublish:
    def test_publish_video_without_media(self, video: Video) -> None:
        with pytest.raises(ValueError, match="Video media is required to publish the video"):
            video.publish()

    def test_publish_video_with_pending_media(self, video: Video) -> None:
        video.video = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location="",
            status=MediaStatus.PROCESSING,
            media_type=MediaType.VIDEO,
        )
        with pytest.raises(ValueError, match="Video must be fully processed to be published"):
            video.publish()

    def test_publish_video_with_completed_media(self, video: Video) -> None:
        video.video = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location="encoded_path",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        video.publish()
        assert video.published is True


class TestUpdateVideoMedia:
    def test_update_video_and_append_event(self, video: Video) -> None:
        media = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location="encoded_path",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        video.update_video_media(media)
        assert video.video == media
        assert video.events == [AudioVideoMediaUpdated(
            aggregate_id=video.id,
            file_path=media.raw_location,
            media_type=MediaType.VIDEO,
        )]

from uuid import uuid4
from decimal import Decimal

import pytest

from src.core.video.domain.value_objects import Rating, ImageMedia, AudioVideoMedia, MediaStatus
from src.core.video.domain.video import Video


class TestVideoEntity:
    def test_valid_video(self):
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            published=True,
            rating=Rating.AGE_12,
            categories={uuid4()},
            genres={uuid4()},
            cast_members={uuid4()},
        )

        # Check if the validation passes without errors
        video.validate()
        assert video.notification.has_errors is False

    def test_invalid_video(self):
        with pytest.raises(ValueError, match="Title is required"):
            video = Video(
                title="",
                description="A test video",
                launch_year=2022,
                duration=Decimal("120.5"),
                published=True,
                rating=Rating.AGE_12,
                categories={uuid4()},
                genres={uuid4()},
                cast_members={uuid4()},
            )

    def test_optional_attributes(self):
        # Create a Video object with optional attributes
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            published=True,
            rating=Rating.AGE_12,
            categories={uuid4()},
            genres={uuid4()},
            cast_members={uuid4()},
            banner=ImageMedia(uuid4(), "checksum", "banner.jpg", "path/to/banner"),
            thumbnail=None,  # Testing None value for an optional attribute
            trailer=AudioVideoMedia(
                uuid4(), "checksum", "trailer.mp4", "raw_path", "encoded_path", MediaStatus.COMPLETED,
            ),
        )
        assert video.notification.has_errors is False

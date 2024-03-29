import uuid
from decimal import Decimal

import pytest

from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import RelatedEntitiesNotFound
from src.core.video.domain.value_objects import Rating
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


@pytest.fixture
def category_repository():
    return InMemoryCategoryRepository()


@pytest.fixture
def video_repository():
    return InMemoryVideoRepository()


@pytest.fixture
def genre_repository():
    return InMemoryGenreRepository()


@pytest.fixture
def cast_member_repository():
    return InMemoryCastMemberRepository()


@pytest.fixture
def use_case(
        category_repository: InMemoryCategoryRepository,
        video_repository: InMemoryVideoRepository,
        genre_repository: InMemoryGenreRepository,
        cast_member_repository: InMemoryCastMemberRepository,
) -> CreateVideoWithoutMedia:
    return CreateVideoWithoutMedia(
        video_repository=video_repository,
        category_repository=category_repository,
        genre_repository=genre_repository,
        cast_member_repository=cast_member_repository,
    )


class TestCreateVideoWithoutMedia:
    def test_create_video_without_media_with_associated_categories(
            self,
            use_case: CreateVideoWithoutMedia,
            category_repository: InMemoryCategoryRepository,
            video_repository: InMemoryVideoRepository,
    ) -> None:
        category_repository.save(Category(name="Category 1", description="Category 1 description"))
        category_repository.save(Category(name="Category 2", description="Category 2 description"))

        output = use_case.execute(
            CreateVideoWithoutMedia.Input(
                title="Video 1",
                description="Video 1 description",
                launch_year=2022,
                opened=True,
                duration=Decimal(120),
                rating=Rating.L,
                categories={cat.id for cat in category_repository.list()},
                genres=set(),
                cast_members=set(),
            )
        )

        assert len(video_repository.list()) == 1
        created_video = video_repository.get_by_id(output.id)
        assert created_video.title == "Video 1"
        assert created_video.description == "Video 1 description"
        assert created_video.launch_year == 2022
        assert created_video.opened
        assert created_video.duration == Decimal(120)
        assert created_video.rating == Rating.L
        assert created_video.categories == {cat.id for cat in category_repository.list()}

    def test_create_video_without_media_with_inexistent_categories_raise_an_error(
        self,
        use_case: CreateVideoWithoutMedia,
        category_repository: InMemoryCategoryRepository,
        video_repository: InMemoryVideoRepository,
    ) -> None:
        with pytest.raises(RelatedEntitiesNotFound, match="Invalid categories") as exc:
            use_case.execute(
                CreateVideoWithoutMedia.Input(
                    title="Video 1",
                    description="Video 1 description",
                    launch_year=2022,
                    opened=True,
                    duration=Decimal(120),
                    rating=Rating.L,
                    categories={uuid.uuid4()},
                    genres=set(),
                    cast_members=set(),
                )
            )

        assert len(video_repository.list()) == 0

from uuid import UUID

from django.db import transaction

from src.core.video.domain.value_objects import AudioVideoMedia, MediaType
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import Video as VideoORM, AudioVideoMedia as AudioVideoMediaORM


class DjangoORMVideoRepository(VideoRepository):
    # TODO: use model/entity mapper
    def save(self, video: Video) -> None:
        with transaction.atomic():
            video_model = VideoORM.objects.create(
                title=video.title,
                description=video.description,
                launch_year=video.launch_year,
                opened=video.opened,
                duration=video.duration,
                rating=video.rating,
            )
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_model = VideoORM.objects.get(id=id)
        except VideoORM.DoesNotExist:
            return None
        else:
            return VideoModelMapper.to_entity(video_model)

    def delete(self, id: UUID) -> None:
        VideoORM.objects.filter(id=id).delete()

    def list(self) -> list[Video]:
        return [VideoModelMapper.to_entity(video) for video in VideoORM.objects.all()]

    def update(self, video: Video) -> None:
        try:
            video_model = VideoORM.objects.get(pk=video.id)
        except VideoORM.DoesNotExist:
            return None
        else:
            with transaction.atomic():
                # Remove related medias - if they exist
                AudioVideoMediaORM.objects.filter(id=video_model.video_id).delete()

                # Persist related medias if they exist in the entity
                video_model.video = AudioVideoMediaORM.objects.create(
                    name=video.video.name,
                    raw_location=video.video.raw_location,
                    encoded_location=video.video.encoded_location,
                    status=video.video.status,
                ) if video.video else None

                # Update relationships with other entities/aggregates
                video_model.categories.set(video.categories)
                video_model.genres.set(video.genres)
                video_model.cast_members.set(video.cast_members)

                # Update video attributes
                video_model.title = video.title
                video_model.description = video.description
                video_model.launch_year = video.launch_year
                video_model.opened = video.opened
                video_model.duration = video.duration
                video_model.rating = video.rating
                video_model.published = video.published

                video_model.save()

class VideoModelMapper:
    @staticmethod
    def to_entity(model: VideoORM) -> Video:
        video = Video(
            id=model.id,
            title=model.title,
            description=model.description,
            launch_year=model.launch_year,
            opened=model.opened,
            duration=model.duration,
            rating=model.rating,
            published=model.published,
            categories=set(model.categories.values_list("id", flat=True)),
            genres=set(model.genres.values_list("id", flat=True)),
            cast_members=set(model.cast_members.values_list("id", flat=True)),
        )

        if model.video:
            video.video = AudioVideoMedia(
                name=model.video.name,
                raw_location=model.video.raw_location,
                encoded_location=model.video.encoded_location,
                status=model.video.status,
                media_type=MediaType.VIDEO,
            )

        return video

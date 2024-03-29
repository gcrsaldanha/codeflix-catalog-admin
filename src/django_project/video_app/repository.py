from uuid import UUID

from django.db import transaction

from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import Video as VideoORM, AudioVideoMedia, ImageMedia


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
            video_model = VideoORM.objects.get(pk=id)
            return Video(
                id=video_model.id,
                title=video_model.title,
                description=video_model.description,
                launch_year=video_model.launch_year,
                opened=video_model.opened,
                duration=video_model.duration,
                rating=video_model.rating,
                categories=set(video_model.categories.values_list("id", flat=True)),
                genres=set(video_model.genres.values_list("id", flat=True)),
                cast_members=set(video_model.cast_members.values_list("id", flat=True)),
            )
        except VideoORM.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        VideoORM.objects.filter(id=id).delete()

    def list(self) -> list[Video]:
        return [
            Video(
                id=video_model.id,
                title=video_model.title,
                description=video_model.description,
                launch_year=video_model.launch_year,
                opened=video_model.opened,
                duration=video_model.duration,
                rating=video_model.rating,
                categories=set(video_model.categories.values_list("id", flat=True)),
                genres=set(video_model.genres.values_list("id", flat=True)),
                cast_members=set(video_model.cast_members.values_list("id", flat=True)),
            ) for video_model in VideoORM.objects.all()
        ]

    def update(self, video: Video) -> None:
        try:
            video_model = VideoORM.objects.get(pk=video.id)
        except VideoORM.DoesNotExist:
            return None
        else:
            with transaction.atomic():
                # Remove related medias - if they exist
                AudioVideoMedia.objects.filter(id=video_model.video_id).delete()

                # Update relationships with other entities/aggregates
                video_model.categories.set(video.categories)
                video_model.genres.set(video.genres)
                video_model.cast_members.set(video.cast_members)

                # Persist related medias if they exist in the entity
                video_model.video = AudioVideoMedia.objects.create(
                    name=video.video.name,
                    raw_location=video.video.raw_location,
                    status=video.video.status,
                ) if video.video else None

                # Update video attributes
                video_model.title = video.title
                video_model.description = video.description
                video_model.launch_year = video.launch_year
                video_model.opened = video.opened
                video_model.duration = video.duration
                video_model.rating = video.rating

                video_model.save()

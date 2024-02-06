from uuid import UUID

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


class DjangoORMGenreRepository(GenreRepository):
    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreORM.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_model.categories.set(genre.categories)

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            # TODO: N+1
            genre_model = GenreORM.objects.get(id=id)
            return Genre(
                id=genre_model.id,
                name=genre_model.name,
                is_active=genre_model.is_active,
                categories=set(genre_model.categories.values_list("id", flat=True)),
            )
        except GenreORM.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        GenreORM.objects.filter(id=id).delete()

    def list(self) -> list[Genre]:
        # TODO: N+1
        return [
            Genre(
                id=genre_model.id,
                name=genre_model.name,
                is_active=genre_model.is_active,
                categories=set(genre_model.categories.values_list("id", flat=True)),
            ) for genre_model in GenreORM.objects.all()
        ]

    def update(self, genre: Genre) -> None:
        try:
            genre_model = GenreORM.objects.get(pk=genre.id)
        except GenreORM.DoesNotExist:
            return None
        else:
            with transaction.atomic():
                GenreORM.objects.filter(pk=genre.id).update(
                    name=genre.name,
                    is_active=genre.is_active,
                )
                genre_model.categories.set(genre.categories)

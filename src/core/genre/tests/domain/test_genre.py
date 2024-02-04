import pytest
from uuid import UUID
import uuid

from src.core.genre.domain.genre import Genre


class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(
                TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            Genre(name="a" * 256)

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre(name="")

    def test_create_genre_with_default_values(self):
        genre = Genre(name="Romance")
        assert isinstance(genre.id, UUID)
        assert genre.name == "Romance"
        assert genre.is_active is True
        assert genre.categories == set()

    def test_create_genre_with_provided_values(self):
        category_id = uuid.uuid4()
        genre_id = uuid.uuid4()
        genre = Genre(
            id=genre_id,
            name="Romance",
            categories={category_id},
            is_active=False,
        )

        assert genre.id == genre_id
        assert genre.name == "Romance"
        assert genre.is_active is False
        assert genre.categories == {category_id}


class TestChangeName:
    def test_change_genre_name(self):
        genre = Genre(name="Romance")
        genre.change_name(name="Drama")
        assert genre.name == "Drama"

    def test_change_to_invalid_name_raises_exception(self):
        genre = Genre(name="Romance")
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            genre.change_name(name="a" * 256)

    def test_cannot_change_to_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre(name="")


class TestActivate:
    def test_activate_inactive_genre(self):
        genre = Genre(
            name="Romance",
            is_active=False,
        )

        assert genre.is_active is False
        genre.activate()
        assert genre.is_active is True

    def test_activate_active_genre(self):
        genre = Genre(
            name="Romance",
            is_active=True,
        )

        assert genre.is_active is True
        genre.activate()
        assert genre.is_active is True


class TestDeactivate:
    def test_deactivate_active_genre(self):
        genre = Genre(
            name="Romance",
            is_active=True,
        )

        assert genre.is_active is True
        genre.deactivate()
        assert genre.is_active is False

    def test_deactivate_inactive_genre(self):
        genre = Genre(
            name="Romance",
            is_active=False,
        )

        assert genre.is_active is False
        genre.deactivate()
        assert genre.is_active is False


class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        genre_1 = Genre(name="Romance", id=common_id)
        genre_2 = Genre(name="Drama", id=common_id)

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        genre = Genre(name="Filme", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert genre != dummy


class TestAddCategory:
    def test_add_category(self):
        genre = Genre(name="Romance")
        category_id = uuid.uuid4()
        genre.add_category(category_id)
        assert genre.categories == {category_id}


class TestRemoveCategory:
    def test_remove_category(self):
        category_id = uuid.uuid4()
        genre = Genre(name="Romance", categories={category_id})
        genre.remove_category(category_id)
        assert genre.categories == set()

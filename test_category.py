import unittest
from uuid import UUID
import uuid

from category import Category


class TestCategory(unittest.TestCase):
    def test_name_is_required(self):
        with self.assertRaisesRegex(TypeError, "missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with self.assertRaisesRegex(ValueError, "name must have less than 256 characters"):
            Category(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name="Filme")
        self.assertEquals(type(category.id), UUID)

    def test_create_category_with_default_values(self):
        category = Category(name="Filme")
        self.assertEquals(category.name, "Filme")
        self.assertEquals(category.description, "")
        self.assertEquals(category.is_active, True)

    def test_create_category_as_active_by_default(self):
        category = Category(name="Filme")
        self.assertEquals(category.is_active, True)

    def test_create_category_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name="Filme",
            description="Filmes em geral",
            is_active=False,
        )
        self.assertEquals(category.id, cat_id)
        self.assertEquals(category.name, "Filme")
        self.assertEquals(category.description, "Filmes em geral")
        self.assertEquals(category.is_active, False)


if __name__ == "__main__":
    unittest.main()


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        # list_url = reverse('category-list')
        url = '/api/categories/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [
            {
                "id": "9bc466a6-b7ca-450c-9c59-033447112676",
                "name": "Movie",
                "description": "Movie description",
                "is_active": True
            },
            {
                "id": "6f7c2133-f1d3-4040-b700-c547453345d3",
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            }
        ]
        assert response.data == expected_data

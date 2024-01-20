from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)
from django_project.category_app.repository import DjangoORMCategoryRepository


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request):
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(request=ListCategoryRequest())

        categories = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active,
            }
            for category in response.data
        ]

        return Response(
            status=HTTP_200_OK,
            data=categories,
        )

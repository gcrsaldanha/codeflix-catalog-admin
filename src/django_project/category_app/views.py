from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from src.core.category.application.use_cases.exceptions import CategoryNotFound

from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)
from core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from django_project.category_app.repository import DjangoORMCategoryRepository


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
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

    def retrieve(self, request: Request, pk: UUID) -> Response:
        try:
            pk = UUID(pk)
        except ValueError:
            return Response(
                status=HTTP_400_BAD_REQUEST, data={"id": ["Enter a valid UUID."]}
            )

        request = GetCategoryRequest(id=pk)
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            response = use_case.execute(request=request)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_200_OK,
            data={
                "id": str(response.id),
                "name": response.name,
                "description": response.description,
                "is_active": response.is_active,
            },
        )

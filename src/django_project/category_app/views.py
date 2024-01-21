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
    ListCategoryResponse,
)
from core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.serializers import ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response: ListCategoryResponse = use_case.execute(request=ListCategoryRequest())
        response_serializer = ListCategoryResponseSerializer(response)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    def retrieve(self, request: Request, pk: UUID) -> Response:
        request_data = RetrieveCategoryRequestSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)

        # request = GetCategoryRequest(id=request_data.validated_data["id"])
        request = GetCategoryRequest(**request_data.validated_data)
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            response = use_case.execute(request=request)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        response_serializer = RetrieveCategoryResponseSerializer(response)
        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

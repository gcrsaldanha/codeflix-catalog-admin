from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
)
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound,
    InvalidCategory,
)

from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
)
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    ListCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
)


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response: ListCategoryResponse = use_case.execute(request=ListCategoryRequest())
        response_serializer = ListCategoryResponseSerializer(response)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    def retrieve(self, request: Request, pk: UUID = None) -> Response:
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

    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(output).data,
        )

    def update(self, request: Request, pk: UUID = None):
        serializer = UpdateCategoryRequestSerializer(data={
            **request.data.dict(),
            "id": pk,
        })
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk: UUID = None):
        pass

    def destroy(self, request, pk: UUID = None):
        pass

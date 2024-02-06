from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
)

from src.core.genre.application.use_cases import (
    ListGenre,
    CreateGenre,
    DeleteGenre,
    UpdateGenre,
)
from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import (
    ListGenreOutputSerializer,
    CreateGenreInputSerializer,
    DeleteGenreInputSerializer,
    CreateGenreOutputSerializer,
)


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Input = use_case.execute(ListGenre.Input())
        response_serializer = ListGenreOutputSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )
        try:
            output = use_case.execute(CreateGenre.Input(**serializer.validated_data))
        except (InvalidGenre, RelatedCategoriesNotFound) as error:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateGenreOutputSerializer(output).data,
        )

    def destroy(self, request: Request, pk: UUID = None):
        request_data = DeleteGenreInputSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)
        input = DeleteGenre.Input(**request_data.validated_data)

        use_case = DeleteGenre(repository=DjangoORMGenreRepository())
        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"Genre with id {pk} not found"},
            )

        return Response(status=HTTP_204_NO_CONTENT)

    def update(self, request: Request, pk: UUID = None):
        pass

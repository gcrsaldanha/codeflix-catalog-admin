from pathlib import Path
from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.django_project.video_app.repository import DjangoORMVideoRepository


class VideoViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        raise NotImplementedError

    def create(self, request: Request) -> Response:
        raise NotImplementedError

    def destroy(self, request: Request, pk: UUID = None):
        raise NotImplementedError

    def update(self, request: Request, pk: UUID = None):
        raise NotImplementedError

    def partial_update(self, request: Request, pk: UUID = None):
        file = request.FILES["video_file"]
        content = file.read()
        content_type = file.content_type

        upload_video = UploadVideo(
            repository=DjangoORMVideoRepository(),
            storage_service=LocalStorage()
        )
        try:
            upload_video.execute(
                UploadVideo.Input(
                    video_id=pk,
                    file_name=file.name,
                    content=content,
                    content_type=content_type
                )
            )
        except VideoNotFound:
            return Response(status=404)

        return Response(status=200)

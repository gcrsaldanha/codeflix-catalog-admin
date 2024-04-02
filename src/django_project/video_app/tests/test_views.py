from unittest.mock import patch
from uuid import uuid4

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from src.core.video.domain.video import Video


@pytest.fixture
def uploaded_file() -> SimpleUploadedFile:
    return SimpleUploadedFile(name='test.mp4', content=b'file_content', content_type='video/mp4')


class TestPartialUpdate:
    def test_when_video_exists_then_(self, video: Video) -> None:
        url = f"/videos/{str(video.id)}/"

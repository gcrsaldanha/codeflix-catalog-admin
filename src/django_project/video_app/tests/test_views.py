import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from src.core.video.domain.video import Video


@pytest.fixture
def uploaded_file() -> SimpleUploadedFile:
    return SimpleUploadedFile(name='test.mp4', content=b'file_content', content_type='video/mp4')


class TestPartialUpdate:
    def test_when_video_exists_then_update_video_and_dispatch_integration_event(self) -> None:
        pass

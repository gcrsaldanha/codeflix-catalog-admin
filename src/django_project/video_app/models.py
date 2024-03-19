from django.db import models

# Create your models here.
from uuid import uuid4

from django.db import models

from src.core.video.domain.value_objects import MediaStatus, Rating


class Video(models.Model):
    RATING_CHOICES = [(rating.name, rating.name) for rating in Rating]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()
    launch_year = models.IntegerField()
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    published = models.BooleanField()
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)

    categories = models.ManyToManyField("category_app.Category", related_name="videos")
    genres = models.ManyToManyField("genre_app.Genre", related_name="videos")
    cast_members = models.ManyToManyField("cast_member_app.CastMember", related_name="videos")

    banner = models.OneToOneField("ImageMedia", null=True, blank=True, on_delete=models.SET_NULL)
    thumbnail = models.OneToOneField(
        "ImageMedia", null=True, blank=True, related_name="video_thumbnail", on_delete=models.SET_NULL
    )
    thumbnail_half = models.OneToOneField(
        "ImageMedia", null=True, blank=True, related_name="video_thumbnail_half", on_delete=models.SET_NULL
    )
    trailer = models.OneToOneField(
        "AudioVideoMedia", null=True, blank=True, related_name="video_trailer", on_delete=models.SET_NULL
    )
    video = models.OneToOneField(
        "AudioVideoMedia", null=True, blank=True, related_name="video_media", on_delete=models.SET_NULL
    )


class ImageMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    checksum = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=255)


class AudioVideoMedia(models.Model):
    STATUS_CHOICES = [(status.name, status.name) for status in MediaStatus]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    checksum = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=255)
    encoded_location = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

from django.contrib import admin
from src.django_project.video_app.models import Video, AudioVideoMedia, ImageMedia

class VideoAdmin(admin.ModelAdmin):
    pass


class AudioVideoMediaAdmin(admin.ModelAdmin):
    pass


class ImageMediaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Video, VideoAdmin)
admin.site.register(AudioVideoMedia, AudioVideoMediaAdmin)
admin.site.register(ImageMedia, ImageMediaAdmin)

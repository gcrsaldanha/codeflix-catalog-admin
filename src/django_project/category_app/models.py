from uuid import uuid4
from django.db import models


class Category(models.Model):
    app_label = "category_app"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name

from django.db import models

from src.basecore.base_model import BaseModel


STORAGE_TYPE_CHOICES = (
    ('temp', 'temp'),
    ('permanent', 'permanent'),
)


class FileStorage(BaseModel):
    type = models.CharField(max_length=128, choices=STORAGE_TYPE_CHOICES)
    destination = models.CharField(max_length=256)

    class Meta:
        db_table = "file_storages"

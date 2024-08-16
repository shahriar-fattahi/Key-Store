from django.db import models


class Storage(models.Model):
    class Meta:
        indexes = [
            models.Index(models.F("data__key"), name="data__key_idx"),
        ]

    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

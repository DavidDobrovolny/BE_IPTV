from django.db import models


# Create your models here.
class Video(models.Model):
    raw = models.JSONField()
    name = models.CharField()
    icon = models.ImageField(upload_to="icons/")
    description = models.TextField(null=True)
    has_subtitles = models.BooleanField()
    is_multilingual = models.BooleanField()
    is_hd = models.BooleanField()
    is_uhd = models.BooleanField()
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

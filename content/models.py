from django.conf import settings
from django.db import models


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=256, unique=True)
    body = models.TextField()

    def __str__(self):
        return f"{self.title}"

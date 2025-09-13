from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=256, unique=True)
    body = models.TextField()

    def __str__(self):
        return f"{self.title}"

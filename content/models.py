from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=256, unique=True)
    body = models.TextField()
    slug = models.SlugField(max_length=300, unique=True, null=False)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_likes', blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

    @property
    def title_length(self):
        return len(self.title.split())

    @property
    def body_length(self):
        return len(self.body.split())

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

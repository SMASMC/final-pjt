import uuid
from django.db import models
from django.conf import settings

class LaterVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='later_videos')
    videoId = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    thumbnailUrl = models.URLField()
    publishedAt = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'videoId')
        ordering = ['-createdAt']

    def __str__(self):
        return f'{self.user} - {self.title}'

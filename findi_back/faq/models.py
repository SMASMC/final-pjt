import uuid
from django.db import models

class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    answer = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

# schedules/models.py

import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

# 색깔 선택 리스트
COLOR_CHOICES = [
    ("#C6AAF1", "Purple"),
    ("#E68181", "Pink"),
    ("#4ECDC4", "Blue"),
    ("#FFE57B", "Yellow"),
    ("#888888", "Grey"),
]

class UserSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 역참조시 related_name
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='schedules')
    title = models.CharField(max_length=150)
    contents = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#C6AAF1') 
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
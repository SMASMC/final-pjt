import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None  # username 필드 제거
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    userName = models.CharField(max_length=150)  # userName 선언 하여 다른 필드로 대체
    age = models.PositiveIntegerField(null=True, blank=True)
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    PLATFORM_CHOICES = [('local', 'Local'), ('google', 'Google'), ('kakao', 'Kakao')]
    loginPlatform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, default='local')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userName']

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profileImage = models.URLField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

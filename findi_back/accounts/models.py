import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import os

# 프로필 이미지 업로드 경로 => 이미있는 파일 삭제
def user_profile_upload_path(instance, filename):
    ext = 'png' # 확장자 고정
    filename = f'{instance.user.email}.{ext}'
    file_path = os.path.join('profiles', filename)

    # 기존 파일 삭제
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_path
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
    
    def __str__(self):
        return self.userName # article과 댓글에서 작성자 정보 위해

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monthly_income = models.PositiveIntegerField(null=True, blank=True)  # 월 소득 (만원)
    savings = models.PositiveIntegerField(null=True, blank=True)         # 모아둔 돈 (만원)
    profileImage = models.ImageField(upload_to=user_profile_upload_path, null=True, blank=True)  # 이미지 파일로 교체

    RISK_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    FINANCE_GOALS = [
        ('saving', 'Saving'),
        ('investment', 'Investment'),
        ('retirement', 'Retirement'),
    ]
    INTEREST_CHOICES = [
        ('deposit', 'Deposit'),
        ('loan', 'Loan'),
        ('insurance', 'Insurance'),
        ('fund', 'Fund'),
    ]

    age = models.PositiveIntegerField(null=True, blank=True)
    risk_tolerance = models.CharField(max_length=10, choices=RISK_CHOICES, default='medium')
    financial_goal = models.CharField(max_length=20, choices=FINANCE_GOALS, default='saving')
    interested_products = models.JSONField(default=list)  # ['deposit', 'fund'] 등

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')




class UserPortfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    productName = models.CharField(max_length=100)
    bankName = models.CharField(max_length=100)
    productType = models.CharField(max_length=100)
    interestRate = models.DecimalField(max_digits=5, decimal_places=2)
    prePaymentPenalty = models.DecimalField(max_digits=5, decimal_places=2)
    joinedAt = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='portfolio')
    
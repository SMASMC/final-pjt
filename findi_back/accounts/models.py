import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import os
from django.contrib.auth.base_user import BaseUserManager
from finance.models import FinancialProduct
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, userName, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, userName=userName, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, userName, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser는 is_staff=True여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser는 is_superuser=True여야 합니다.')

        return self.create_user(email, userName, password, **extra_fields)



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
    age = models.IntegerField(null=True, blank=True)
    PLATFORM_CHOICES = [('local', 'Local'), ('google', 'Google'), ('kakao', 'Kakao')]
    loginPlatform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, default='local')
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin')], default='user')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userName']
    objects = CustomUserManager()
    
    def __str__(self):
        return self.userName # article과 댓글에서 작성자 정보 위해

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monthly_income = models.IntegerField(null=True, blank=True)  # 월 소득 (만원)
    savings = models.IntegerField(null=True, blank=True)         # 모아둔 돈 (만원)
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

    age = models.IntegerField(null=True, blank=True)
    risk_tolerance = models.CharField(max_length=10, choices=RISK_CHOICES, default='medium')
    financial_goal = models.CharField(max_length=20, choices=FINANCE_GOALS, default='saving')
    interested_products = models.JSONField(default=list)  # ['deposit', 'fund'] 등

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

class UserPortfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='portfolio')
    product = models.ForeignKey(FinancialProduct, on_delete=models.CASCADE, related_name='portfolios', null=True, blank=True)
    joinedAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.userName} - {self.product.name}"
    
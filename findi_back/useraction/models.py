import uuid
from django.db import models
from accounts.models import CustomUser
from finance.models import DepositSavings

class FavoriteBank(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    bank = models.ForeignKey(DepositSavings, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

class RecentlyViewed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recently_viewed')
    bank = models.ForeignKey(DepositSavings, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

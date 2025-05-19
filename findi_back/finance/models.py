import uuid
from django.db import models

class DepositSavings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bankName = models.CharField(max_length=100)
    productCode = models.CharField(max_length=50)
    productName = models.CharField(max_length=100)
    etcNote = models.TextField(null=True, blank=True)

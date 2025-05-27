from django.db import models

# Create your models here.

class Commodities(models.Model):
    COMMODITIES_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
    ]
    date = models.DateField()
    metal_type = models.CharField(max_length=10, choices=COMMODITIES_CHOICES)
    close = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()

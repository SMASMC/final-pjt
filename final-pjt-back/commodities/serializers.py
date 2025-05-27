from rest_framework import serializers
from .models import Commodities

class CommoditiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodities
        fields = '__all__'

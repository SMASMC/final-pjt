# videos/serializers.py

from rest_framework import serializers
from .models import LaterVideo

class LaterVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaterVideo
        fields = '__all__'
        read_only_fields = ('user',)
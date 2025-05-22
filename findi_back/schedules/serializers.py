from rest_framework import serializers
from .models import UserSchedule

class UserScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSchedule
        fields = '__all__'
        read_only_fields = ['user', 'createdAt', 'updatedAt']
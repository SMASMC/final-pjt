# articles/serializers.py

from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import CustomUserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'views', 'created_at')

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and hasattr(request, "user") and obj.user == request.user


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article', 'created_at')

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and hasattr(request, "user") and obj.user == request.user
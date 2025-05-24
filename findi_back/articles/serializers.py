# articles/serializers.py

from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import CustomUserSerializer

# 게시글
class ArticleSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'views', 'created_at')


# 댓글
class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

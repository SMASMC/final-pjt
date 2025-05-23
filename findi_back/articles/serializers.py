from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    # user 필드는 문자열로 읽기만 가능 (프론트에서 작성자 이름 확인용)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'views', 'created_at')

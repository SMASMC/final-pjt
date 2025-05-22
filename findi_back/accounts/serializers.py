from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['access_token'] = str(refresh.access_token)
        data['refresh_token'] = str(refresh)

        # 사용자 객체에서 필요한 정보만 뽑아 추가
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'nickname': self.user.nickname if hasattr(self.user, 'nickname') else '',
        }

        return data
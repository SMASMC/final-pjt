from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import UserProfile, CustomUser, UserPortfolio
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from accounts.models import UserPortfolio
from finance.models import DepositProduct, SavingProduct

User = get_user_model()

# 로그인 serializer
class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        # email과 password를 가져옴
        email = attrs.get('email')
        password = attrs.get('password')

        # 사용자 인증
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('이메일 또는 비밀번호가 올바르지 않습니다.')

        self.user = user  #  명시적으로 self.user 지정
        return attrs

# 회원 가입시 필요한 serializer
class CustomRegisterSerializer(RegisterSerializer):
    userName = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['userName'] = self.validated_data.get('userName', '')
        print(f'cleaned data: {data}')
        return data

    def save(self, request):
        user = super().save(request)
        user.userName = self.cleaned_data.get('userName')
        user.save()
        print(f'saved user: {user}')
        return user


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
            'userName': self.user.userName,
        }
        print(f'validated data: {data}')
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'age',
            'monthly_income',
            'savings',
            'risk_tolerance',
            'financial_goal',
            'interested_products',
            'profileImage',
            'createdAt',
            'updatedAt'
        ]

class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'userName', 'loginPlatform', 'profile','role']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'userName', 'email', 'role', 'loginPlatform')

# 프로필 업데이트 serializer
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'profileImage', 'age', 'risk_tolerance', 'monthly_income', 'savings',
            'financial_goal', 'interested_products'
        ]
        

# 예적금 serializer
class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = [
            'fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'save_trm',
            'intr_rate', 'intr_rate2','spcl_cnd'
        ]


class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = [
            'fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'save_trm',
            'intr_rate', 'intr_rate2','spcl_cnd'
        ]


# 사용자 포트폴리오 serializer
class UserPortfolioSerializer(serializers.ModelSerializer):
    deposit_product = DepositProductSerializer(read_only=True)
    saving_product = SavingProductSerializer(read_only=True)

    bank_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = UserPortfolio
        fields = [
            'id',
            'product_type',
            'deposit_product',
            'saving_product',
            'bank_name',
            'product_name',
            'save_trm',
            'interest_rate',
            'special_rate',
            'etc_note', 
            'joined_at',
        ]

    def get_bank_name(self, obj):
        if obj.product_type == 'deposit' and obj.deposit_product:
            return obj.deposit_product.kor_co_nm
        elif obj.product_type == 'saving' and obj.saving_product:
            return obj.saving_product.kor_co_nm
        return '[상품 없음]'

    def get_product_name(self, obj):
        if obj.product_type == 'deposit' and obj.deposit_product:
            return obj.deposit_product.fin_prdt_nm
        elif obj.product_type == 'saving' and obj.saving_product:
            return obj.saving_product.fin_prdt_nm
        return '[상품 없음]'
    

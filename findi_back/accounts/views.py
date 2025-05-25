from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import UserProfile
from django.utils import timezone
from django.db import transaction
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from django.core.cache import cache
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserWithProfileSerializer, CustomRegisterSerializer, CustomLoginSerializer, UserProfileUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from dj_rest_auth.views import LoginView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserPortfolio
from .serializers import UserPortfolioSerializer
import uuid
from django.core.files.base import ContentFile


# CustomLoginView의 선언 이유는?
# 이 클래스는 기본 LoginView의 응답에 사용자 정보를 추가하고 싶을 때 사용
class CustomLoginView(LoginView):
    permission_classes = [AllowAny]
    serializer_class = CustomLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.user  # 로그인된 사용자
        refresh = RefreshToken.for_user(user)
        user_data = UserWithProfileSerializer(user).data

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': user_data
        }, status=status.HTTP_200_OK)
    
# CustomTokenObtainPairView의 선언 이유는? 
# 이 클래스는 기본 TokenObtainPairView의 응답에 사용자 정보를 추가하고 싶을 때 사용
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 회원가입을 위한 view
class CustomRegisterView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        # 회원가입 시리얼라이저로 유효성 검사
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 사용자 생성
        user = serializer.save(request)

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)

        # 직렬화된 사용자 + 프로필 정보
        user_data = UserWithProfileSerializer(user).data

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': user_data
        }, status=status.HTTP_201_CREATED)

load_dotenv()
User = get_user_model()

# 환경변수 캐싱
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
FRONTEND_OAUTH_CALLBACK_URL = os.getenv("FRONTEND_OAUTH_CALLBACK_URL")

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

# google oauth 구현
def google_login(request):
    params = urlencode({
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
    })
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?{params}")


@api_view(['GET'])
@authentication_classes([])
@transaction.atomic
def google_login_callback(request):
    code = request.GET.get("code")
    if not code:
        return Response({"error": "No code provided"}, status=400)

    # 1. 구글 OAuth 토큰 요청
    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
    )

    if token_res.status_code != 200:
        return Response({"error": "Failed to fetch token from Google"}, status=400)

    access_token = token_res.json().get("access_token")
    if not access_token:
        return Response({"error": "No access token returned from Google"}, status=400)

    # 2. 사용자 정보 요청
    user_info = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    email = user_info.get("email")
    name = user_info.get("name")
    profile_image = user_info.get("picture")

    if not email:
        return Response({"error": "No email in user info"}, status=400)

    # 3. 사용자 생성 또는 조회
    user, created = User.objects.get_or_create(email=email, defaults={
        "userName": name,
        "loginPlatform": "google",
    })

    if created:
        user.set_unusable_password()
        user.save()
        profile = UserProfile(user=user)
        # ✅ 프로필 이미지 다운로드 후 저장
        if profile_image:
            response = requests.get(profile_image)
            if response.status_code == 200:
                ext = profile_image.split('.')[-1].split('?')[0]
                file_content = ContentFile(response.content)
                # 여기서는 save()에서 filename은 자동으로 upload_to 함수에서 처리
                profile.profileImage.save(f"temp.{ext}", file_content, save=False)  # 이름은 무시됨
        profile.save()

    # 4. JWT 발급
    refresh = RefreshToken.for_user(user)
    access_token_jwt = str(refresh.access_token)
    refresh_token_jwt = str(refresh)

    # 5. 프론트로 리디렉션
    params = urlencode({
        "access_token": access_token_jwt,
        "refresh_token": refresh_token_jwt,
    })
    return redirect(f"{FRONTEND_OAUTH_CALLBACK_URL}?{params}")

# kakao oauth 구현
def kakao_login(request):
    params = urlencode({
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "response_type": "code",
        "scope": "account_email profile_nickname profile_image",
        "prompt": "login"
    })
    return redirect(f"https://kauth.kakao.com/oauth/authorize?{params}")


@api_view(['GET'])
@authentication_classes([])
@transaction.atomic
def kakao_login_callback(request):
    code = request.GET.get("code")
    if not code:
        return Response({"error": "No code provided"}, status=400)

    # 1. 액세스 토큰 요청
    token_response = requests.post("https://kauth.kakao.com/oauth/token", data={
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    if token_response.status_code != 200:
        return Response({"error": "Failed to get token from Kakao"}, status=400)

    access_token = token_response.json().get("access_token")
    if not access_token:
        return Response({"error": "No access token received"}, status=400)

    # 2. 사용자 정보 요청
    user_info_response = requests.get("https://kapi.kakao.com/v2/user/me", headers={
        "Authorization": f"Bearer {access_token}"
    })

    user_info = user_info_response.json()
    kakao_account = user_info.get("kakao_account", {})

    email = kakao_account.get("email")
    nickname = kakao_account.get("profile", {}).get("nickname")
    profile_image_url = kakao_account.get("profile", {}).get("profile_image_url")

    if not email:
        return Response({"error": "이메일 동의가 필요합니다."}, status=400)

    # 3. 사용자 생성 또는 조회
    user, created = User.objects.get_or_create(email=email, defaults={
        "userName": nickname,
        "loginPlatform": "kakao",
    })

    if created:
        user.set_unusable_password()
        user.save()
        profile = UserProfile(user=user)

        # ✅ 프로필 이미지 다운로드 후 저장
        if profile_image_url:
            response = requests.get(profile_image_url)
            if response.status_code == 200:
                ext = profile_image_url.split('.')[-1].split('?')[0]
                file_content = ContentFile(response.content)
                # 여기서는 save()에서 filename은 자동으로 upload_to 함수에서 처리
                profile.profileImage.save(f"temp.{ext}", file_content, save=False)  # 이름은 무시됨
        profile.save()

    # 4. JWT 발급
    refresh = RefreshToken.for_user(user)
    jwt_access = str(refresh.access_token)
    jwt_refresh = str(refresh)

    # 5. 프론트로 리디렉션
    params = urlencode({
        "access_token": jwt_access,
        "refresh_token": jwt_refresh,
    })

    return redirect(f"{FRONTEND_OAUTH_CALLBACK_URL}?{params}")



@api_view(['POST'])
def send_code(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': '이메일이 필요합니다.'}, status=400)

    code = str(random.randint(100000, 999999))
    cache.set(f'verify_code:{email}', code, timeout=300)  # 5분 유효

    # HTML 렌더링
    subject = 'Findi 비밀번호 찾기 인증코드'
    from_email = 'msoko89@gmail.com'
    to = [email]
    text_content = f'인증번호는 {code}입니다.'
    html_content = f"""
                    <html>
                    <body>
                        <h2 style="color: #8A69E1;">Findi 인증번호</h2>
                        <p>비밀번호 재설정을 위해 아래 인증번호를 입력해 주세요.</p>
                        <div style="
                            font-size: 20px;
                            font-weight: bold;
                            background: #8A69E1;
                            color: white;
                            padding: 10px 20px;
                            border-radius: 6px;
                            display: inline-block;
                            margin-top: 10px;">
                            {code}
                        </div>
                        <p style="margin-top: 20px; color: #888;">이 인증번호는 5분간 유효합니다.</p>
                    </body>
                    </html>
                    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return Response({'message': '인증번호가 전송되었습니다.'})

@api_view(['POST'])
def verify_code(request):
    email = request.data.get('email')
    code = request.data.get('code')

    saved_code = cache.get(f'verify_code:{email}')
    if saved_code == code:
        return Response({'verified': True})
    return Response({'verified': False}, status=400)

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(email, password)

    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return Response({'success': True})
    except User.DoesNotExist:
        return Response({'error': '사용자를 찾을 수 없습니다.'}, status=404)

# 사용자 Profile + user 조회
# @api_view(['GET', 'PUT'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def user_profile(request):
#     # UserProfile이 없으면 생성
#     profile, _ = UserProfile.objects.get_or_create(user=request.user)

#     # GET: 프로필 정보 반환
#     if request.method == 'GET':
#         serializer = UserProfileUpdateSerializer(profile)
#         return Response(serializer.data)

#     # PUT: 프로필 정보 수정
#     if request.method == 'PUT':
#         serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def user_profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    # ✅ GET: User + Profile 데이터 반환
    if request.method == 'GET':
        serializer = UserWithProfileSerializer(user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': serializer.data
        }, status=200)

    # ✅ PUT: UserProfile 정보 수정
    if request.method == 'PUT':
        serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


# 사용자 포트폴리오 관련 view
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_portfolio(request):
    if request.method == 'GET':
        portfolios = UserPortfolio.objects.filter(user=request.user)
        serializer = UserPortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': '상품 ID가 필요합니다.'}, status=400)

        try:
            product = FinancialProduct.objects.get(id=product_id)
        except FinancialProduct.DoesNotExist:
            return Response({'error': '해당 상품이 존재하지 않습니다.'}, status=404)

        portfolio, created = UserPortfolio.objects.get_or_create(
            user=request.user,
            product=product,
        )
        if not created:
            return Response({'message': '이미 가입한 상품입니다.'}, status=200)

        return Response({'message': '상품 가입 완료'}, status=201)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_portfolio_detail_and_update(request, fin_prdt_cd):
    try:
        portfolio = UserPortfolio.objects.get(user=request.user, fin_prdt_cd=fin_prdt_cd)
    except UserPortfolio.DoesNotExist:
        return Response({'error': '포트폴리오를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserPortfolioSerializer(portfolio)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserPortfolioSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_portfolio_delete(request, fin_prdt_cd):
    try:
        portfolio = UserPortfolio.objects.get(user=request.user, fin_prdt_cd=fin_prdt_cd)
    except UserPortfolio.DoesNotExist:
        return Response({'error': '포트폴리오를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    portfolio.delete()
    return Response({'message': '포트폴리오가 삭제되었습니다.'}, status=status.HTTP_200_OK)



# 회원 탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user

    try:
        user.delete()
        return Response({'message': '회원 탈퇴가 완료되었습니다.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
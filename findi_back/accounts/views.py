from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, authentication_classes
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
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


load_dotenv()
User = get_user_model()

# 환경변수 캐싱
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
FRONTEND_OAUTH_CALLBACK_URL = os.getenv("FRONTEND_OAUTH_CALLBACK_URL")


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
        "createdAt": timezone.now(),
        "updatedAt": timezone.now(),
    })

    if created:
        user.set_unusable_password()
        user.save()
        UserProfile.objects.create(
            user=user,
            profileImage=profile_image,
            createdAt=timezone.now(),
            updatedAt=timezone.now(),
        )

    # 4. JWT 발급
    refresh = RefreshToken.for_user(user)
    access_token_jwt = str(refresh.access_token)
    refresh_token_jwt = str(refresh)

    # 5. 프론트로 리디렉션
    params = urlencode({
        "access_token": access_token_jwt,
        "refresh_token": refresh_token_jwt,
        "email": user.email,
        "userName": user.userName,
        "profileImage": profile_image,
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
    html_content = render_to_string('emails/verify_code.html', {'code': code})

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

    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return Response({'success': True})
    except User.DoesNotExist:
        return Response({'error': '사용자를 찾을 수 없습니다.'}, status=404)
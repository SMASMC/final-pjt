from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls'), name='rest_auth'),  # 로그인/로그아웃/비밀번호
    path('auth/registration/', include('dj_rest_auth.registration.urls'), name='rest_auth_registration'),  # 회원가입
    path('google/login/', views.google_login, name='google_login'),  # 소셜 OAuth 로그인
    path('google/login/callback/', views.google_login_callback, name='google_login_callback'),  # 소셜 OAuth 콜백

    # 비밀번호 찾기 관련 URL
    path('send-code/', views.send_code, name='send_code'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
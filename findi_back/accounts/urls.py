from django.urls import path, include
from . import views
from .views import CustomRegisterView, CustomLoginView

app_name = "accounts"

urlpatterns = [
    # auth/login/을 먼저 선언하고 따로 사용하는 이유는 dj_rest_auth.urls에서 custom으로 login을 사용하기 때문
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'), # 먼저 선언
    path('auth/', include('dj_rest_auth.urls')),  # 로그인/로그아웃/비밀번호
    path('auth/registration/', CustomRegisterView.as_view(), name='rest_auth_registration'),  # 회원가입

    path('google/login/', views.google_login, name='google_login'),  # 소셜 OAuth 로그인
    path('google/login/callback/', views.google_login_callback, name='google_login_callback'),  # 소셜 OAuth 콜백

    # 비밀번호 찾기 관련 URL
    path('send-code/', views.send_code, name='send_code'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # 사용자 정보 관련 URL
    path('profile/', views.user_profile, name='user_profile'),
]

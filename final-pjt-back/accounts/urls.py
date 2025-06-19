from django.urls import path, include
from . import views
from .views import CustomRegisterView, CustomLoginView, refresh_token_cookie

app_name = "accounts"

urlpatterns = [
    # auth/login/을 먼저 선언하고 따로 사용하는 이유는 dj_rest_auth.urls에서 custom으로 login을 사용하기 때문
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'), # 먼저 선언
    path("auth/logout/", views.logout_view, name="logout"),
    path('auth/', include('dj_rest_auth.urls')),  # 로그인/로그아웃/비밀번호
    path('auth/registration/', CustomRegisterView.as_view(), name='rest_auth_registration'),  # 회원가입
    path("auth/refresh/", refresh_token_cookie, name="refresh_token"),
    # Google OAuth
    path('google/login/', views.google_login, name='google_login'),  # 소셜 OAuth 로그인
    path('google/login/callback/', views.google_login_callback, name='google_login_callback'),  # 소셜 OAuth 콜백

    # Kakao OAuth
    path('kakao/login/', views.kakao_login, name='kakao_login'),  # 소셜 OAuth 로그인
    path('kakao/login/callback/', views.kakao_login_callback, name='kakao_login_callback'),  # 소셜 OAuth 콜백

    # 비밀번호 찾기 관련 URL
    path('send-code/', views.send_code, name='send_code'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # 사용자 정보 관련 URL
    path('profile/', views.user_profile, name='user_profile'),

    # 사용자 포트폴리오 관련 URL
    path('portfolio/', views.user_portfolio, name='user_portfolio'),
    path('portfolio/<uuid:portfolio_id>/', views.user_portfolio_detail_and_update, name='user_portfolio_detail'),
    path('portfolio/<uuid:portfolio_id>/delete/', views.user_portfolio_delete, name='user_portfolio_delete'),

    # 회원 탈퇴
    path('delete-account/', views.delete_account, name='delete_account'),
]

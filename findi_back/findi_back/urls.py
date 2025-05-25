"""
URL configuration for findi_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# JWT 인증, 인가를 위한 패키지
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import CustomTokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    
    # JWT 인증, 인가를 위한 URL
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 금융감독원 API를 이용한 데이터 + 맞춤 상품
    path('finance/', include('finance.urls'), name='finance'),
    # 영상
    path('videos/', include('videos.urls'), name='videos'),
    # 게시글
    path('articles/', include('articles.urls')),
    # 카카오맵
    path('kakaomap/', include('kakaomap.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

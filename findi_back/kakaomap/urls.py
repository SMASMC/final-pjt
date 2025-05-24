from django.urls import path
from .views import kakao_key_view

urlpatterns = [
    path('kakao-key/', kakao_key_view),
]
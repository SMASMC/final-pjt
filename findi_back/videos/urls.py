# videos/urls.py

from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('later-videos/', views.later_video_list_create),
    path('later-videos/<str:videoId>/', views.later_video_delete),
]

from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list_create),
    path('<uuid:pk>/', views.article_detail),
    path('<uuid:pk>/increment-views/', views.increment_views),
    path('api/upload_image/', views.upload_image),
]
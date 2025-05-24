from django.urls import path
from . import views

urlpatterns = [
    # 게시글
    path('', views.article_list_create, name='article_list_create'),
    path('<uuid:pk>/', views.article_detail, name='article_detail'),
    path('<uuid:pk>/increment-views/', views.increment_views, name='article_increment_views'),

    # 댓글
    path('<uuid:article_id>/comments/', views.comment_list_create, name='comment_list_create'),
    path('<uuid:article_id>/comments/<uuid:comment_id>/', views.comment_update_or_delete, name='comment_update_or_delete')
] 

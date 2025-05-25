from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    # 상품 조회
    path('banks/products/', views.banks_products, name="banks_products"),

    # 맞춤 상품 추천
    path('find-fit-products/', views.find_fit_product, name="find_fit_product"),
    path('find-ai-fit-products/', views.find_ai_fit_product, name="find_ai_fit_product"),

    path('deposit/', views.deposit_get, name="deposit_get"),
    path('saving/', views.saving_get, name="saving_get"),
    path('rent/', views.rent_get, name="rent_get"),
    path('credit/', views.credit_get, name="credit_get"),
]

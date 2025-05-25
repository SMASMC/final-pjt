from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    # path('', views.finance_list, name="finance_list"),
    # path('<str:fin_prdt_cd>/', views.finance_detail_and_update, name="finance_detail_and_update"),
    # path('<str:fin_prdt_cd>/delete/', views.finance_delete, name="finance_delete"),
    path('find-fit-products/', views.find_fit_product, name="find_fit_product"),
    path('find-ai-fit-products/', views.find_ai_fit_product, name="find_ai_fit_product"),

    path('deposit/', views.deposit_get, name="deposit_get"),
    path('saving/', views.saving_get, name="saving_get"),
    path('rent/', views.rent_get, name="rent_get"),
    path('credit/', views.credit_get, name="credit_get"),
]

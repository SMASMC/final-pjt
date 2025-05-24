from django.urls import path, include
from . import views
app_name = "finance"

urlpatterns = [
    path('', views.finance_get, name="finance_get"),
]

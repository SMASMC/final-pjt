from django.urls import path
from .views import commodity_prices

app_name = 'commodities'

urlpatterns = [
    path('', commodity_prices, name='commodity_prices'),
]

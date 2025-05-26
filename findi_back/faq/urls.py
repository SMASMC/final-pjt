from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    path('ask/', views.ask_faq, name='ask_faq'),
]

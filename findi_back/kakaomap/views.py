from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import os

def kakao_key_view(request):
    return JsonResponse({
        'kakao_key': os.getenv('KAKAO_JAVASCRIPT_KEY')
    })
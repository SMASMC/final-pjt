from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import ArticleSerializer
import os
from datetime import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# 게시글 전체 조회 와 생성
#IsAuthenticatedOrReadOnly 데코레이터는 PUT.POST.DELETE의 요청에 로그인이 필요하다는 거임

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def article_list_create(request):
    if request.method == 'GET':
        search = request.query_params.get('search')
        if search:
            articles = Article.objects.filter(title__icontains=search).order_by('-created_at')
        else:
            articles = Article.objects.all().order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 이미지 업로드 함수
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        ext = os.path.splitext(image.name)[1]  # .jpg, .png 등
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        filename = f"{timestamp}{ext}"
        upload_dir = 'uploads/'  # media/uploads/
        filepath = os.path.join(upload_dir, filename)

        saved_path = default_storage.save(filepath, ContentFile(image.read()))
        image_url = settings.MEDIA_URL + saved_path
        return JsonResponse({'url': image_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# 게시글 상세 조회와 수정 및 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # 요청자와 작성자가 동일한지 확인하기
    if request.user != article.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 조회수 증가 로직
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def increment_views(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.views += 1
    article.save()
    return Response({'views': article.views})
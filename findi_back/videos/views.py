# videos/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import LaterVideo
from .serializers import LaterVideoSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def later_video_list_create(request):
    print(f'request.data {request.data}')
    if request.method == 'GET':
        videos = LaterVideo.objects.filter(user=request.user)
        print(f'videos : {videos}')
        serializer = LaterVideoSerializer(videos, many=True)
        print(f'serializer : {serializer.data}')

        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = LaterVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def later_video_detail_and_delete(request, videoId):
    try:
        video = LaterVideo.objects.get(user=request.user, videoId=videoId)
    except LaterVideo.DoesNotExist:
        if request.method == 'GET':
            return Response({'isSaved': False})
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response({'isSaved': True})

    if request.method == 'DELETE':
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


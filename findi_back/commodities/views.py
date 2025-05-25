from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Commodities
from .serializers import CommoditiesSerializer

@api_view(['GET'])
def commodity_prices(request):
    metal = request.GET.get('metal', 'gold')  # 기본값 gold
    start = request.GET.get('start')  # YYYY-MM-DD
    end = request.GET.get('end')

    queryset = Commodities.objects.filter(metal_type=metal)

    if start and end:
        queryset = queryset.filter(date__range=[start, end])
    elif start or end:
        return Response({'error': '시작일과 종료일 모두 입력해야 합니다.'}, status=400)

    queryset = queryset.order_by('date')
    serializer = CommoditiesSerializer(queryset, many=True)
    return Response(serializer.data)

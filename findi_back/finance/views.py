from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from dotenv import load_dotenv

load_dotenv()

# Create your views here.
# finance_get는 FINANCIAL_SUPERVISORY_API_KEY를 이용하여 금융상품 정보를 가져오는 API

BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
FINANCIAL_SUPERVISORY_API_KEY = os.getenv("FINANCIAL_SUPERVISORY_API_KEY")

@api_view(['GET'])
def finance_get(request):
    pass
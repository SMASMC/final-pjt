from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import os
from dotenv import load_dotenv
from accounts.models import UserProfile
from finance.models import FinancialProduct, DepositProduct, SavingProduct, CreditLoanProduct, RentHouseLoanProduct
from finance.serializers import DepositProductSerializer, SavingProductSerializer, CreditLoanProductSerializer, RentHouseLoanProductSerializer
from rest_framework.pagination import PageNumberPagination


from openai import OpenAI
load_dotenv()

# Create your views here.I

BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
FINANCIAL_SUPERVISORY_API_KEY = os.getenv("FINANCIAL_SUPERVISORY_API_KEY")

# @api_view(['GET'])
# def finance_list(request):
#     """
#     금융상품 리스트 반환
#     """


# def finance_detail_and_update(request, fin_prdt_cd):
#     """
#     금융상품 상세 정보 반환
#     """    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_fit_product(request):
    """
    사용자 정보 기반으로 추천 금융상품 반환
    """
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    # JSON 데이터 불러오기 (캐싱된 finance_info.json 기준)
    json_path = os.path.join(os.path.dirname(__file__), '../../finance_info.json')
    if not os.path.exists(json_path):
        return Response({"error": "금융 데이터가 존재하지 않습니다."}, status=500)

    with open(json_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    # 1. 관심 상품군 필터링
    interested_types = profile.interested_products or []
    if not interested_types:
        return Response({"error": "관심 있는 상품 유형을 먼저 설정해주세요."}, status=400)

    filtered = [p for p in products if p['type'] in interested_types]

    # 2. 위험 성향에 따른 정렬
    if profile.risk_tolerance == 'low':
        filtered = sorted(filtered, key=lambda x: x.get('interest_rate', 0))
    elif profile.risk_tolerance == 'high':
        filtered = sorted(filtered, key=lambda x: x.get('max_interest_rate', 0), reverse=True)
    else:  # medium
        filtered = sorted(filtered, key=lambda x: x.get('interest_rate', 0), reverse=True)

    # 3. 유형별로 상위 하나씩만 추출
    recommended = {}
    for product in filtered:
        t = product['type']
        if t not in recommended:
            recommended[t] = product

    return Response({"recommendations": list(recommended.values())})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_ai_fit_product(request):
    from openai import OpenAI

    user = request.user

    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return Response({"error": "프로필이 없습니다. 먼저 프로필을 작성해주세요."}, status=404)

    # 전체 카테고리
    categories = ['deposit', 'saving']
    top_products = {}

    # 상품 조회 (카테고리별 top 3)
    for category in categories:
        # 상품별 유효금리로 정렬 (내림차순)
        products = FinancialProduct.objects.filter(product_type=category).order_by('-intr_rate2')[:3]
        if not products:
            return Response({"error": f"{category} 상품이 부족합니다. 관리자에게 문의해주세요."}, status=500)
        top_products[category] = list(products)
    # 사용자 요약
    summary = (
        f"{user.userName}님은 {profile.age}세이며, 월 소득은 {profile.monthly_income}만원, "
        f"모아둔 돈은 {profile.savings}만원입니다. "
        f"현재 재무 목표는 '{profile.financial_goal}'이고 위험 선호도는 '{profile.risk_tolerance}'입니다."
    )

    # GPT용 프롬프트
    def build_product_section(products, label):
        section = [f"{label} 상품 목록:"]
        for i, p in enumerate(products, 1):
            rate = p.intr_rate2
            section.append(
                f"{i}. 이름: {p.name}, 금리: {rate}%, 설명: {p.details or '없음'}, 링크: /products/{p.fin_prdt_cd}"
            )
        return '\n'.join(section)

    prompt_parts = [summary, "아래에 예금, 적금 상품들이 제공됩니다.\n각 금융 상품 유형별로 사용자에게 가장 적합한 상품을 하나씩 골라 추천해주세요.\n친절하고 신뢰감 있게 설명해주세요."]
    prompt_parts.append(build_product_section(top_products['deposit'], "💰 예금"))
    prompt_parts.append(build_product_section(top_products['saving'], "💸 적금"))

    prompt = "\n\n".join(prompt_parts)

    # GPT 호출
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 신뢰할 수 있는 금융 상품 추천 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        ai_message = response.choices[0].message.content
    except Exception as e:
        return Response({"error": f"GPT 추천 생성 실패: {str(e)}"}, status=500)

    # GPT가 추천한 상품 이름 찾기
    recommended_names = []
    for cat in ['deposit', 'saving']:
        for product in top_products[cat]:
            if product.name in ai_message:
                recommended_names.append((cat, product))
                break

    # 추천된 상품 정보를 요약해서 프론트에 전달
    summary_products = {}
    for cat, product in recommended_names:
        summary_products[cat] = {
            "name": product.name,
            "rate": float(product.intr_rate2 or 0),
            "details": product.details,
            "link": f"/products/{product.fin_prdt_cd}"
        }

    return Response({
        "products": summary_products,
        "ai_recommendation": ai_message
    })


class ShortPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

# 예금 조회
@api_view(['GET'])
def deposit_get(request):
    queryset = DepositProduct.objects.all()
    bank = request.GET.get('bank')
    save_trm = request.GET.get('save_trm')
    ordering = request.GET.get('ordering')
    if ordering:
        queryset = queryset.order_by(ordering)
    if bank:
        queryset = queryset.filter(kor_co_nm__icontains=bank)
    if save_trm:
        queryset = queryset.filter(save_trm=save_trm)

    paginator = ShortPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = DepositProductSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


# 적금 조회
@api_view(['GET'])
def saving_get(request):
    queryset = SavingProduct.objects.all()
    bank = request.GET.get('bank')
    save_trm = request.GET.get('save_trm')
    ordering = request.GET.get('ordering')
    if ordering:
        queryset = queryset.order_by(ordering)
    if bank:
        queryset = queryset.filter(kor_co_nm__icontains=bank)
    if save_trm:
        queryset = queryset.filter(save_trm=save_trm)

    paginator = ShortPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = SavingProductSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


# 대출 조회
@api_view(['GET'])
def credit_get(request):
    queryset = CreditLoanProduct.objects.all()
    bank = request.GET.get('bank')
    if bank:
        queryset = queryset.filter(kor_co_nm__icontains=bank)
    serializer = CreditLoanProductSerializer(queryset, many=True)
    return Response(serializer.data)

# 전세자금대출 조회
@api_view(['GET'])
def rent_get(request):
    queryset = RentHouseLoanProduct.objects.all()
    bank = request.GET.get('bank')
    if bank:
        queryset = queryset.filter(kor_co_nm__icontains=bank)
    serializer = RentHouseLoanProductSerializer(queryset, many=True)
    return Response(serializer.data)

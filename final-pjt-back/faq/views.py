from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv
from django.conf import settings
import json
from openai import OpenAI

load_dotenv()

@api_view(['POST'])
def ask_faq(request):
    question = request.data.get("question")
    if not question:
        return Response({"error": "질문이 필요합니다."}, status=400)

    faq_path = os.path.join(settings.BASE_DIR, "faq", "chatbot", "faq_data.json")

    faq_list = []
    faq_prompt_intro = ""
    try:
        with open(faq_path, encoding='utf-8') as f:
            faq_data = json.load(f)
            faq_list = faq_data.get("faq", [])

            # 질문과 정확히 일치하는 항목이 있으면 그 즉시 반환
            for item in faq_list:
                if item['question'].strip() == question.strip():
                    return Response({"answer": item["answer"]})

            faq_prompt_intro = "아래는 Findi 서비스에 대한 자주 묻는 질문과 답변입니다:\n\n"
            for item in faq_list:
                faq_prompt_intro += f"Q: {item['question']}\nA: {item['answer']}\n\n"
    except Exception as e:
        print(f"[FAQ 로딩 실패]: {str(e)}")

    # 2. 고정 질문 유사도 매칭
    from difflib import SequenceMatcher
    for item in faq_list:
        similarity = SequenceMatcher(None, question.strip(), item["question"].strip()).ratio()
        if similarity > 0.9:
            return Response({"answer": item["answer"]})

    # 3. GPT 호출
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "당신은 'Findi'라는 개인 맞춤형 금융 상품 추천 플랫폼에 대해 잘 알고 있는 금융 상담 챗봇입니다. "
                        "사용자의 질문에 대해 친절하고 신뢰감 있게 안내하세요.\n\n"
                        + faq_prompt_intro
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.8
        )
        answer = response.choices[0].message.content
        return Response({"answer": answer})
    except Exception as e:
        return Response({"error": f"답변 생성 실패: {str(e)}"}, status=500)

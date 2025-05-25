from django.apps import AppConfig
from django.core.management import call_command
import os
import json
from django.conf import settings
from django.db.utils import OperationalError
from django.db import connections

class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'

    def ready(self):
        try:
            # DB 연결이 가능한지 먼저 확인 (마이그레이션 직후 대비)
            connections['default'].cursor()

            from finance.models import FinancialProduct
            if FinancialProduct.objects.exists():
                return

            json_path = os.path.join(settings.BASE_DIR, 'finance', 'data_cache', 'finance_info.json')
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        FinancialProduct.objects.get_or_create(
                            fin_prdt_cd=item['fin_prdt_cd'],
                            defaults={
                                'name': item['name'],
                                'product_type': item['product_type'],
                                'interest_rate': item['interest_rate'],
                                'details': item.get('details', '')
                            }
                        )
                print("✅ JSON 기반 금융상품 초기화 완료")
            else:
                print("📡 금융상품 JSON 없음 → API fetch 및 등록 시작")
                call_command('fetch_finance_data')
                call_command('create_products_from_json')

        except OperationalError:
            print("🚫 금융상품 초기화 skipped (DB 준비되지 않음)")
        except Exception as e:
            print(f"⚠️ 금융상품 초기화 중 예외 발생: {e}")

import requests
import json
import os
from dotenv import load_dotenv
from django.conf import settings
from django.core.management.base import BaseCommand
from finance.models import FinancialCompany, FinancialProduct
from decimal import Decimal
from django.apps import apps

load_dotenv()

FINANCIAL_SUPERVISORY_API_KEY = os.getenv("FINANCIAL_SUPERVISORY_API_KEY")
BASE_URL = "https://finlife.fss.or.kr/finlifeapi"

ENDPOINTS = {
    'deposit': 'depositProductsSearch.json',
    'saving': 'savingProductsSearch.json',
    'rent': 'rentHouseLoanProductsSearch.json',
    'credit': 'creditLoanProductsSearch.json'
}

model_name_map = {
    'deposit': 'DepositProduct',
    'saving': 'SavingProduct',
    'rent': 'RentHouseLoanProduct',
    'credit': 'CreditLoanProduct',
}

def get_model_fields(model_name):
    model = apps.get_model('finance', model_name)
    return set([field.name for field in model._meta.fields])

class Command(BaseCommand):
    help = "Fetch and store finance product data from FSS API"

    def handle(self, *args, **kwargs):
        for category, endpoint in ENDPOINTS.items():
            cache_dir = os.path.join(settings.BASE_DIR, 'finance', 'data_cache')
            os.makedirs(cache_dir, exist_ok=True)
            json_path = os.path.join(cache_dir, f'finance_cache_{category}.json')

            url = f"{BASE_URL}/{endpoint}"
            params = {
                'auth': FINANCIAL_SUPERVISORY_API_KEY,
                'topFinGrpNo': '020000',
                'pageNo': 1
            }

            res = requests.get(url, params=params)
            if res.status_code != 200:
                self.stdout.write(self.style.ERROR(f"[Error] {category} API 요청 실패"))
                continue

            data = res.json()
            base_list = data.get('result', {}).get('baseList', [])
            option_list = data.get('result', {}).get('optionList', [])

            best_options = {}
            for opt in option_list:
                fin_prdt_cd = opt.get('fin_prdt_cd')
                if not fin_prdt_cd:
                    continue

                if category == 'rent':
                    target_rate = opt.get('lend_rate_avg')
                elif category == 'credit':
                    target_rate = opt.get('crdt_grad_avg')
                else:
                    target_rate = opt.get('intr_rate2')

                try:
                    rate = Decimal(str(target_rate))
                except:
                    rate = None

                if rate is not None:
                    current = best_options.get(fin_prdt_cd)
                    current_rate = current['rate'] if current else Decimal('-1')
                    if rate > current_rate:
                        best_options[fin_prdt_cd] = {
                            'rate': rate,
                            'opt': opt
                        }

            merged_data = []
            model_fields = get_model_fields(model_name_map[category])

            for item in base_list:
                fin_prdt_cd = item.get('fin_prdt_cd')
                best = best_options.get(fin_prdt_cd, {})
                best_opt = best.get('opt', {})

                merged_item = {**item}

                if category in ['deposit', 'saving']:
                    merged_item.update({
                        'save_trm': best_opt.get('save_trm'),
                        'intr_rate_type': best_opt.get('intr_rate_type'),
                        'intr_rate_type_nm': best_opt.get('intr_rate_type_nm'),
                        'intr_rate': float(best_opt.get('intr_rate') or 0),
                        'intr_rate2': float(best_opt.get('intr_rate2') or 0),
                    })
                elif category == 'rent':
                    merged_item.update({
                        'save_trm': best_opt.get('save_trm'),
                        'crdt_grad_avg': float(best_opt.get('crdt_grad_avg') or 0)
                    })
                elif category == 'credit':
                    merged_item.update({
                        'save_trm': best_opt.get('save_trm'),
                        'lend_rate_avg': float(best_opt.get('lend_rate_avg') or 0)
                    })

                cleaned_item = {k: v for k, v in merged_item.items() if k in model_fields}
                merged_data.append(cleaned_item)

                # 회사 저장
                company, _ = FinancialCompany.objects.get_or_create(
                    code=item['fin_co_no'],
                    defaults={'name': item['kor_co_nm']}
                )

                # FinancialProduct 저장
                FinancialProduct.objects.update_or_create(
                    fin_prdt_cd=fin_prdt_cd,
                    defaults={
                        'name': item['fin_prdt_nm'],
                        'company': company,
                        'product_type': category,
                        'intr_rate2': Decimal(str(merged_item.get('intr_rate2'))) if category in ['deposit', 'saving'] else None,
                        'lend_rate_avg': Decimal(str(merged_item.get('lend_rate_avg'))) if category == 'credit' else None,
                        'crdt_grad_avg': Decimal(str(merged_item.get('crdt_grad_avg'))) if category == 'rent' else None,
                        'details': item.get('etc_note', '')
                    }
                )

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, ensure_ascii=False, indent=2)

            self.stdout.write(self.style.SUCCESS(f" {category} 저장 완료"))

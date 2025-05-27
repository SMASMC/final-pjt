from django.core.management.base import BaseCommand
import json
from finance.models import DepositProduct, SavingProduct, RentHouseLoanProduct, CreditLoanProduct

class Command(BaseCommand):
    help = 'Load deposit, saving, rent, credit data from JSON into DB (중복 방지 포함)'

    def handle(self, *args, **options):
        def load_and_save(model, file_path):
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
            saved_count = 0
            skipped_count = 0
            for item in data:
                if model.objects.filter(fin_prdt_cd=item.get('fin_prdt_cd')).exists():
                    skipped_count += 1
                    continue
                model.objects.create(**item)
                saved_count += 1
            self.stdout.write(self.style.SUCCESS(
                f"{model.__name__}: 저장됨={saved_count}, 중복건수={skipped_count}"
            ))

        load_and_save(DepositProduct, 'finance/data_cache/finance_cache_deposit.json')
        load_and_save(SavingProduct, 'finance/data_cache/finance_cache_saving.json')
        load_and_save(RentHouseLoanProduct, 'finance/data_cache/finance_cache_rent.json')
        load_and_save(CreditLoanProduct, 'finance/data_cache/finance_cache_credit.json')

        self.stdout.write(self.style.SUCCESS(' 전체 금융 상품 데이터 저장 완료!'))
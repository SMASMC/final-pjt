from enum import unique
import uuid
from django.db import models


class FinancialCompany(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class FinancialProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PRODUCT_TYPES = [
        ('deposit', '정기예금'),
        ('savings', '적금'),
        ('rent', '전세자금대출'),
        ('credit', '개인신용대출'),
    ]
    # TODO : 연금저축, 주택담보대출 추가 예정
    # ('pension', '연금저축'),
    # ('mortgage', '주택담보대출'),
    company = models.ForeignKey(FinancialCompany, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='default')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='deposit')
    # 상품 유형별 금리
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 예/적금
    lend_rate_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 전세대출
    crdt_grad_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 신용대출
    fin_prdt_cd = models.CharField(max_length=20, unique=True, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def get_effective_rate(self):
        if self.product_type == 'deposit' or self.product_type == 'savings':
            return self.intr_rate2
        elif self.product_type == 'rent':
            return self.lend_rate_avg
        elif self.product_type == 'credit':
            return self.crdt_grad_avg
        return None


# 예금
class DepositProduct(models.Model):
    dcls_month = models.CharField(max_length=6, null=True, blank=True)  # 공시일
    fin_co_no = models.CharField(max_length=20, null=True, blank=True)  # 금융회사코드
    fin_prdt_cd = models.CharField(max_length=20,unique=True,null=True,blank=True)  # 금융상품코드
    kor_co_nm = models.CharField(max_length=50)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100)  # 금융상품명
    join_way = models.TextField()  # 가입방법
    mtrt_int = models.TextField()  # 이자율
    spcl_cnd = models.TextField()  # 특이사항
    join_deny = models.CharField(max_length=1, null=True, blank=True)  # 가입금지
    join_member = models.TextField()  # 가입대상
    etc_note = models.TextField()  # 기타사항
    max_limit = models.CharField(max_length=100, null=True, blank=True)  # 최대한도
    dcls_strt_day = models.CharField(max_length=8)  # 공시시작일
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True)  # 공시종료일
    fin_co_subm_day = models.CharField(max_length=20)  # 제출일
    save_trm = models.CharField(max_length=10, null=True, blank=True)
    intr_rate_type = models.CharField(max_length=10, null=True, blank=True)
    intr_rate_type_nm = models.CharField(max_length=50, null=True, blank=True)
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

# 적금
class SavingProduct(models.Model):
    dcls_month = models.CharField(max_length=6, null=True, blank=True) # 공시일
    fin_co_no = models.CharField(max_length=20, null=True, blank=True)
    fin_prdt_cd = models.CharField(max_length=20,unique=True,null=True,blank=True)
    kor_co_nm = models.CharField(max_length=50)
    fin_prdt_nm = models.CharField(max_length=100)
    join_way = models.TextField()  # 가입방법
    mtrt_int = models.TextField()  # 이자율
    spcl_cnd = models.TextField()  # 특이사항
    join_deny = models.CharField(max_length=1, null=True, blank=True)  # 가입금지
    join_member = models.TextField()  # 가입대상
    etc_note = models.TextField()  # 기타사항
    max_limit = models.CharField(max_length=100, null=True, blank=True)
    dcls_strt_day = models.CharField(max_length=8)
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True)
    fin_co_subm_day = models.CharField(max_length=20)
    save_trm = models.CharField(max_length=10, null=True, blank=True)
    intr_rate_type = models.CharField(max_length=10, null=True, blank=True)
    intr_rate_type_nm = models.CharField(max_length=50, null=True, blank=True)
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


# 개인신용대출
class CreditLoanProduct(models.Model):
    dcls_month = models.CharField(max_length=6, null=True, blank=True) # 공시일
    fin_co_no = models.CharField(max_length=20, null=True, blank=True)
    fin_prdt_cd = models.CharField(max_length=50,unique=True,null=True,blank=True)
    crdt_prdt_type = models.CharField(max_length=10)
    crdt_prdt_type_nm = models.CharField(max_length=50)
    kor_co_nm = models.CharField(max_length=50)
    fin_prdt_nm = models.CharField(max_length=100)
    join_way = models.TextField()  # 가입방법
    cb_name = models.CharField(max_length=50)  # 공시일
    dcls_strt_day = models.CharField(max_length=8)
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True)
    fin_co_subm_day = models.CharField(max_length=20)
    save_trm = models.CharField(max_length=10, null=True, blank=True)
    lend_rate_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


# 전세자금대출
class RentHouseLoanProduct(models.Model):
    dcls_month = models.CharField(max_length=6, null=True, blank=True) # 공시일
    fin_co_no = models.CharField(max_length=20, null=True, blank=True)
    fin_prdt_cd = models.CharField(max_length=20,unique=True,null=True,blank=True)
    kor_co_nm = models.CharField(max_length=50)
    fin_prdt_nm = models.CharField(max_length=100)
    join_way = models.TextField()  # 가입방법
    loan_inci_expn = models.TextField()  # 공시일
    erly_rpay_fee = models.TextField()
    dly_rate = models.TextField()
    loan_lmt = models.CharField(max_length=100)
    dcls_strt_day = models.CharField(max_length=8)
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True)
    fin_co_subm_day = models.CharField(max_length=20)
    save_trm = models.CharField(max_length=10, null=True, blank=True)
    crdt_grad_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

import uuid
from django.db import models


# 여기에 이제 금융감독원 api를 받아와서 저장할 데이터를 확인 후 저장해서 조회할 수 있도록 기능구현하기
# user의 맞춤상품 테이블이 따로 있어야 할듯하다.

class DepositSavings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bankName = models.CharField(max_length=100)
    productCode = models.CharField(max_length=50)
    productName = models.CharField(max_length=100)
    etcNote = models.TextField(null=True, blank=True)

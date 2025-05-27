# finance/serializers.py
from rest_framework import serializers
from .models import DepositProduct, SavingProduct, CreditLoanProduct, RentHouseLoanProduct


class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'


class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'


class CreditLoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditLoanProduct
        fields = '__all__'

class RentHouseLoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentHouseLoanProduct
        fields = '__all__'

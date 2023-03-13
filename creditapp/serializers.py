from rest_framework import serializers
from .models import Customer, Transaction,TransactionSummary, Score



class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['name', 'bvn', 'phone']


class TransactionSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Transaction
        fields = ['customer', 'transaction_date', 'transaction_type', 'transaction_amount']



class TransactionSummarySerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = TransactionSummary
        fields = '__all__'


class CustomerScoreSerializer(serializers.ModelSerializer):
    Customer= CustomerSerializer()

    class Meta:
        model = Score
        field = "__all__"
  
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from creditapp.models import Customer,Transaction
from rest_framework.test import APITestCase
from decimal import Decimal



class CustomerDataViewTestCase(APITestCase):
    def setUp(self):
        self.bvn = '12345678910'
        self.customer = Customer.objects.create(bvn=self.bvn)

    def test_customer_data_view(self):
        url = reverse('customer_data', kwargs={'bvn': self.bvn})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('bvn'), self.bvn)

    def test_get_customer_data_not_found(self):
        url = reverse('customer_data', kwargs={'bvn': "not_existing"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CustomerTransactionsViewTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(bvn="123456789", name="John doe")
        self.transaction1 = Transaction.objects.create(
            customer=self.customer,
            transaction_type="CREDIT",
            transaction_amount=Decimal("100.0")
        )
        self.transaction2 = Transaction.objects.create(
            customer=self.customer,
            transaction_type="DEBIT",
            transaction_amount=Decimal("200.0")
        )

    def test_get_customer_transactions(self):
        url = reverse('customer_transactions', kwargs={'bvn': self.customer.bvn})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TransactionSerializer([self.transaction1, self.transaction2], many=True).data)

    def test_get_customer_transactions_not_found(self):
        url = reverse('customer_transactions', kwargs={'bvn': "not_existing"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


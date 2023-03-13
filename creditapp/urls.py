from django.urls import path
from .views import CustomerDataView, CustomerTransactionsView, CustomerTransactionSummaryView, CustomerScoreView

urlpatterns = [
    path('customer/<str:bvn>/', CustomerDataView.as_view(), name='customer_data'),
    path('customer/<str:bvn>/transactions/', CustomerTransactionsView.as_view(), name='customer_transactions'),
    path('customer/<str:bvn>/transaction-summary/',  CustomerTransactionSummaryView.as_view(), name='customer_summary'),
    path('customer/<str:bvn>/score/', CustomerScoreView.as_view(), name = 'customers_score')
]
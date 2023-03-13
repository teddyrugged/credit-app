from rest_framework import generics,status
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.exceptions import NotFound, APIException
from rest_framework.response import Response
from .models import Customer, Transaction,TransactionSummary
from .serializers import CustomerSerializer, TransactionSerializer,TransactionSummarySerializer


class CustomerDataView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'bvn'

    def get_object(self):
        bvn = self.kwargs.get('bvn')
        try:
            customer = self.queryset.get(bvn=bvn)
        except Customer.DoesNotExist:
            raise NotFound(detail="Bvn doesn't exist" )
        except Exception as e:
            raise APIException(detail='AUnexpected API error' % str(e))

        return customer



class CustomerTransactionsView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


    def get_queryset(self):
        try:
            customer = Customer.objects.get(bvn=self.kwargs['bvn'])
        except Customer.DoesNotExist:
            raise NotFound(detail="Bvn doesn't exist" )
        except Exception as e:
            raise APIException(detail='AUnexpected API error' % str(e))

        return self.queryset.filter(customer=customer)


class CustomerTransactionSummaryView(generics.ListAPIView):
    serializer_class = TransactionSummarySerializer

    def get_queryset(self):
        try:
            bvn = self.kwargs.get('bvn')
            customer = Customer.objects.get(bvn=self.kwargs['bvn'])
            transactions = Transaction.objects.filter(customer=customer)
            credit_sum = transactions.filter(transaction_type='CREDIT').aggregate(Sum('transaction_amount'))['transaction_amount__sum']
            debit_sum = transactions.filter(transaction_type='DEBIT').aggregate(Sum('transaction_amount'))['transaction_amount__sum']
            credit_count = transactions.filter(transaction_type='CREDIT').count()
            debit_count = transactions.filter(transaction_type='DEBIT').count()
            return [{
                'customer': customer,
                'credit_sum': credit_sum,
                'debit_sum': debit_sum,
                'credit_count': credit_count,
                'debit_count': debit_count
            }]
        except Customer.DoesNotExist:
            raise APIException(detail="Bvn doesn't exist" )
        except Exception as e:
            raise APIException(detail='AUnexpected API error' )







class CustomerScoreView(generics.RetrieveAPIView):
    queryset = Transaction.objects.select_related("customer").all()
    serializer_class = CustomerSerializer

    def retrieve(self, request, *args, **kwargs):
        # customer = get_object_or_404(self.queryset, kwargs['bvn'])
        transactions = self.queryset.filter(bvn=kwargs.get('bvn'))
        credit_scores = transactions.filter(transaction_type="Credit")
        debit_scores = transactions.filter(transaction_type="Debit")
        # {"month1":[{week1:week1data}]}

        def calculate_score(self, start_date, end_date):
            transactions = Transaction.objects.filter(
            customer=self.customer,
            date__range=(start_date, end_date)
        )

        dates = pd.date_range(start_date, end_date, freq='W')
        weeks = [(d, d + timedelta(days=7)) for d in dates]

        avg_credits = []
        avg_debits = []
        for start, end in weeks:
            week_transactions = transactions.filter(date__range=(start, end))
            credits = week_transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum']
            debits = week_transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum']
            if credits is None:
                avg_credits.append(0)
            else:
                avg_credits.append(credits / 7)
            if debits is None:
                avg_debits.append(0)
            else:
                avg_debits.append(debits / 7)

        ratio = np.sum(avg_credits) / np.sum(avg_debits)
        self.score = int(100 / (1 + np.exp(-ratio)))
        self.save()

        # Calculate the average weekly credits and debits
        # start_date = "2022-04-01"
        # end_date = "2022-06-30"
        # weekly_credits = []
        # weekly_debits = []
        # for transaction in transactions:
        #     if start_date <= str(transaction.transaction_date.date()) <= end_date:
        #         if transaction.transaction_type == "Credit":
        #             weekly_credits.append(transaction.transaction_amount)
        #         else:
        #             weekly_debits.append(transaction.transaction_amount)

        # avg_weekly_credits = np.mean(weekly_credits)
        # avg_weekly_debits = np.mean(weekly_debits)

        # # Calculate the ratio of the sum of average weekly credits to the sum of average weekly debits
        # ratio = avg_weekly_credits / avg_weekly_debits

        # # Apply the Sigmoid Function to the ratio
        # score = scipy.special.expit(ratio) * 100

        # # Update the customer's credit score
        # customer.score = int(score)
        # customer.save()

        # return Response({'score': score})






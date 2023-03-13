from django.contrib import admin

# Register your models here.
from .models import Customer,Transaction,TransactionSummary,Score
admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(TransactionSummary)
admin.site.register(Score)
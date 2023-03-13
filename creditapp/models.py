from django.db import models
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=255)
    bvn = models.CharField(max_length=20, primary_key=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "customer"
        ordering = ("created_at",)

    def __str__(self):
         return f'{self.bvn} - {self.name}'


class Transaction(models.Model):

    TRANSACTION_TYPE = [
        ('CREDIT', 'Credit'),
        ('DEBIT', 'Debit'),
    ]
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="customer",
    )
    transaction_date = models.DateTimeField()
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE,
        )
    transaction_amount = models.FloatField()

    def __str__(self):
         return f'{self.customer.name} - {self.transaction_amount} - {self.transaction_type}'


class TransactionSummary(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )
    credit_sum = models.FloatField()
    debit_sum = models.FloatField()
    credit_count = models.IntegerField()
    debit_count = models.IntegerField()

    def __str__(self):
        return self.customer



class Score(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )
    score = models.PositiveSmallIntegerField()


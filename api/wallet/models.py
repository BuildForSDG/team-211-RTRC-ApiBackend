from django.db import models
import uuid
from django.conf import settings


class Wallet(models.Model):
    """Every user account has a wallet created for them on sign up"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="Core Wallet", max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_wallet')
    balance = models.BigIntegerField(default=0.00)
    active = models.BooleanField(default=True)
    currency = models.CharField(max_length=4, default='GHC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.balance)


class Deposit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, default="pending")
    wallet = models.ForeignKey(Wallet,  on_delete=models.CASCADE, related_name='wallet_deposits')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name='user_deposit')
    method = models.CharField(max_length=150, default='bank')
    ref_code = models.CharField(unique=False, editable=False, max_length=250)
    amount = models.BigIntegerField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Transaction(models.Model):
    """ Transactions that occur in each wallet"""
    TRANSACTION_TYPE = (
        ('CREDIT', 'credit'),
        ('DEBIT', 'debit')
      )

    TRANSACTION_STATUS = (
        ('PENDING', 'pending'),
        ('SUCCESS', 'success'),
        ('CANCELLED', 'cancelled'),
        ('FLAGGED', 'flagged'),
      )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey('Wallet', related_name='wallet_transactions', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPE)
    status = models.CharField(max_length=30, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    reference_code = models.CharField(unique=True, editable=False, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.reference_code)



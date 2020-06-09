from django.contrib import admin
from .models import Transaction, Deposit, Wallet

admin.site.register(Transaction)
admin.site.register(Deposit)
admin.site.register(Wallet)

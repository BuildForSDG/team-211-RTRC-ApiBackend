from rest_framework import serializers
from api.users.serializers import UserSerializer
from .models import Wallet, Deposit, Transaction
from django.contrib.auth import get_user_model
import random
User = get_user_model()
from api.tolls.serializers import TollSerializer


class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Wallet
        fields = ['id',
                  'user',
                  'balance',
                  'created_at', 'updated_at']
        read_only_fields = ('id', 'user', 'balance', 'created_at', 'updated_at',)    


class DepositSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = Deposit
        fields = ['id',
                  'user',
                  'wallet',
                  'status',
                  'method',
                  'ref_code',
                  'amount',
                  'created_at',
                  'updated_at', ]
        read_only_fields = ('id',)


class AdminDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
        fields = ['id',
                  'user',
                  'wallet',
                  'status',
                  'method',
                  'ref_code',
                  'amount',
                  'created_at',
                  'updated_at', ]


class TransactionSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)
    toll = TollSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'wallet', 'toll', 'transaction_type', 'amount',
            'reference_code', 'status', 'created_at', 'updated_at']

from rest_framework import serializers
from bills_api.users.serializers import UserSerializer
from .models import Wallet, Deposit, Transaction
from django.contrib.auth import get_user_model
import random
User = get_user_model()


class WalletModelSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Wallet
        fields = ['id',
                  'user',
                  'balance',
                  'created_at', ]
        read_only_fields = ('id', 'user', 'balance', 'created_at')    


class DepositModelSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Deposit
        fields = ['id',
                  'user',
                  'status',
                  'method',
                  'ref_code',
                  'amount',
                  'created_at',
                  'modified', ]


class AdminDepositModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
        fields = ['id',
                  'user',
                  'status',
                  'method',
                  'ref_code',
                  'amount',
                  'created_at',
                  'modified', ]


class TransactionModelSerializer(serializers.ModelSerializer):
    wallet = WalletModelSerializer()
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'wallet', 'transaction_type', 'amount',
            'reference_code', 'status', 'created_at']

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth import get_user_model
import secrets
from api.wallet.serializers import (
    WalletSerializer, AdminDepositSerializer,
    DepositSerializer, TransactionSerializer
)
from api.wallet.models import (
    Wallet, Deposit, Transaction,
)
import api.wallet.constants as const
User = get_user_model()

from rest_framework.decorators import action

from api.wallet.utils import confirm_payment


class WalletViewSet(ModelViewSet):
    model = Wallet
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.all()

    def get_queryset(self):
        """get all transactions from this user's wallet """
        return Wallet.objects.filter(user=self.request.user.id).order_by('-created_at')

    @action(detail=True, methods=['GET'])
    def transactions(self, request, pk=None):
        wallet = self.get_object()
        transactions = Transaction.objects.filter(wallet=wallet)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DepositViewSet(ModelViewSet):
    model = Deposit
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]
    queryset = Deposit.objects.all()

    def get_queryset(self):
        """get all transactions from this user's wallet """
        return Deposit.objects.filter(user=self.request.user.id).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        wallet = Wallet.objects.get(user=request.user)
        ref_code = secrets.token_hex(10)
        while Deposit.objects.filter(ref_code=ref_code).exists():
            ref_code = secrets.token_hex(10)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user, wallet=wallet, method='paystack',
            ref_code=ref_code, status=const.PENDING
            )
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['POST'])
    def confirm(self, request):
        if not confirm_payment(request.data['reference']):
            return Response({ 'detail': 'PAYMENT CONFIRMATION FAILED' }, status=status.HTTP_400_BAD_REQUEST)
        else:
            instance = Deposit.objects.get(ref_code=request.data['reference'])
            instance.status = const.SUCCESS
            instance.save()
            # update wallet balance
            wallet = Wallet.objects.get(user=request.user)
            wallet.balance += instance.amount
            wallet.save()
            serializer = self.get_serializer(instance)
            headers = self.get_success_headers(serializer.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK, headers=headers)


class AdminDepositViewSet(ModelViewSet):
    model = Deposit
    serializer_class = AdminDepositSerializer
    permission_classes = [IsAdminUser]
    queryset = Deposit.objects.all()


class TransactionViewSet(ModelViewSet):
    model = Transaction
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)


class AdminTransactionViewSet(ModelViewSet):
    model = Transaction
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]
    queryset = Transaction.objects.all()

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth import get_user_model
import secrets
from wallet.serializers import *
from wallet.models import *

User = get_user_model()

from rest_framework.decorators import action


class WalletModelViewSet(ModelViewSet):
    model = Wallet
    serializer_class = WalletModelSerializer
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.all()

    def get_queryset(self):
        """get all transactions from this user's wallet """
        return Wallet.objects.filter(user=self.request.user.id).order_by('-created_at')

    @action(detail=True, methods=['GET'])
    def transactions(self, request, pk=None):
        wallet = self.get_object()
        transactions = Transaction.objects.filter(wallet=wallet)
        serializer = TransactionModelSerializer(transactions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DepositModelViewSet(ModelViewSet):
    model = Deposit
    serializer_class = DepositModelSerializer
    permission_classes = [IsAuthenticated]
    queryset = Deposit.objects.all()

    def get_queryset(self):
        """get all transactions from this user's wallet """
        return Deposit.objects.filter(user=self.request.user.id).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        user = request.user
        wallet = Wallet.objects.get(user=user.id)
        amount = request.data['amount']
        ref_code = secrets.token_hex(3)
        method = request.data['method']
        Deposit.objects.create(user=request.user, wallet=wallet, method=method, amount=amount, ref_code=ref_code)
        return Response({"success": "Your deposit request has been received"}, status=status.HTTP_201_CREATED)


class AdminDepositModelViewSet(ModelViewSet):
    model = Deposit
    serializer_class = AdminDepositModelSerializer
    permission_classes = [IsAdminUser]
    queryset = Deposit.objects.all()

    @action(detail=False, methods=['post'])
    def approve_deposit(self, request):
        """
        Approve a payment request
        1. get the deposit request
        2. get the wallet
        3. fund the wallet
        4. Change the status of the request
        5. email the user to inform them of a successful deposit
        """
        deposit = Deposit.objects.get(id=['id'])
        wallet = Wallet.objects.get(id=deposit.wallet.id)
        wallet.balance += deposit.amount
        wallet.save()
        deposit.status = "completed"
        deposit.save()
        return Response({'message': 'Successfully processed payment'}, status=status.HTTP_200_OK)


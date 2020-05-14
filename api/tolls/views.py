from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser
)
from rest_framework.decorators import action
from datetime import datetime

# django imports
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from api.users.permissions import IsCollector, IsUser
from api.users.models import User
from .models import TollLocation, Toll
from .serializers import TollLocationSerializer, TollSerializer
import api.tolls.contants as const
from api.vehicles.models import Vehicle
from api.wallet.models import Wallet, Transaction
import secrets

class TollLocationViewSet(ReadOnlyModelViewSet):
    model = TollLocation
    serializer_class = TollLocationSerializer
    permission_classes = [IsUser]
    queryset = TollLocation.objects.filter(active=True)


class AdminTollLocationViewSet(ModelViewSet):
    model = TollLocation
    serializer_classs = TollLocationSerializer
    permission_classes = [IsAdminUser]
    queryset = TollLocation.objects.all()

    @action(detail=True, methods=['POST'])
    def assign(self, request, pk=None):
        instance = self.get_object()
        collector = User.objects.get(id=request.data['collector'])

        # verify if collector already assigned to another location.
        all_locations = TollLocation.objects.filter(active=True)
        for loc in all_locations:
            if collector in loc.collectors.all():
                if loc.id != instance.id:
                    return Response({
                        'message': 'Collector Already Assigned to ' + str(loc.name),
                    }, status=status.HTTP_400_BAD_REQUEST)

        instance.collectors.add(collector)
        instance.save()
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK, headers=headers)
    
    @action(detail=True, methods=['POST'])
    def remove(self, request, *args, **kwargs):
        instance = self.get_object()
        collector = User.objects.get(id=request.data['collector'])
        instance.collectors.remove(collector)
        instance.save()
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK, headers=headers)


class TollViewSet(ReadOnlyModelViewSet):
    model = Toll
    serializer_class = [TollSerializer]
    permission_classes = [IsUser, IsCollector]

    def get_queryset(self):
        if self.request.user.is_user:
            return self.model.objects.filter(vehicle__user=self.request.user)
            
        elif self.request.user.is_collector:
            return self.model.objects.filter(collector=self.request.user)

    @action(detail=False, methods=['POST'], permission_classes=[IsCollector,], url_path='confirm-payment')
    def confirm_payment(self, request):
        vehicle = Vehicle.objects.get(id=request.data['vehicle'])
        wallet = Wallet.objects.get(user=vehicle.user)

        if wallet.balance < vehicle.category.toll_fee:
            return Response({'detail': 'Insufficient Funds in Wallet'}, status=status.HTTP_400_BAD_REQUEST)
        elif wallet.balance >= vehicle.category.toll_fee:
            instance = Toll()
            instance.vehicle = vehicle
            instance.paid_on = datetime.now()
            instance.status = const.PAID
            instance.collector = request.user
            
            # deduct toll fee from wallet
            wallet.balance -= vehicle.category.toll_fee
            wallet.save()
            instance.save()

            # Log Transaction
            Transaction.objects.create(
                wallet=wallet, transaction_type='DEBIT',
                status='PAID',amount=vehicle.category.toll_fee,
                reference_code=secrets.token_hex(10)
            )
            serializer = self.get_serializer(instance)
            headers = self.get_success_headers(serializer.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK, headers=headers)


class AdminTollViewSet(ModelViewSet):
    model = Toll
    serializer_class = TollSerializer
    permission_classes = [IsAdminUser]
    queryset = Toll.objects.all()


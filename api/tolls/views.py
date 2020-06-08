from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)
from rest_framework.decorators import action
from datetime import datetime

# django imports
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.shortcuts import get_object_or_404
from api.users.permissions import IsCollector, IsUser
from api.users.models import User
from .models import TollLocation, Toll
from .serializers import TollLocationSerializer, TollSerializer
import api.tolls.contants as const
import api.tolls.utils as u
from api.vehicles.models import Vehicle
from api.wallet.models import Wallet, Transaction
import secrets

class TollLocationViewSet(ReadOnlyModelViewSet):
    model = TollLocation
    serializer_class = TollLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_user:
            return TollLocation.objects.filter(active=True)
        else:
            return TollLocation.objects.filter(collectors__id=self.request.user.id)


class AdminTollLocationViewSet(ModelViewSet):
    model = TollLocation
    serializer_class = TollLocationSerializer
    permission_classes = [IsAdminUser]
    queryset = TollLocation.objects.all()

    @action(detail=True, methods=['POST', 'PUT'])
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
    
    @action(detail=True, methods=['POST', 'PUT'])
    def remove(self, request, *args, **kwargs):
        instance = self.get_object()
        collector = User.objects.get(id=request.data['collector'])
        instance.collectors.remove(collector)
        instance.save()
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK, headers=headers)


class TollViewSet(ModelViewSet):
    model = Toll
    serializer_class = [TollSerializer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_user:
            return Toll.objects.filter(vehicle__user=self.request.user)
        else:
            return Toll.objects.filter(collector=self.request.user)

    @action(detail=False, methods=['POST'], permission_classes=[IsCollector], url_path='confirm-payment')
    def confirm_payment(self, request):
        vehicle = Vehicle.objects.get(id=request.data['vehicle'])
        location = TollLocation.objects.get(id=request.data['location'])
        wallet = Wallet.objects.get(user=vehicle.user)

        if wallet.balance < vehicle.category.toll_fee:
            return Response({'detail': 'Insufficient Funds in Wallet'}, status=status.HTTP_400_BAD_REQUEST)
        elif wallet.balance >= vehicle.category.toll_fee:
            instance = Toll()
            instance.vehicle = vehicle
            instance.paid_on = datetime.now()
            instance.status = const.PAID
            instance.reference = u.unique_hashid()
            instance.collector = request.user
            instance.location = location
            instance.save()
            
            # deduct toll fee from wallet
            wallet.balance -= vehicle.category.toll_fee
            wallet.save()

            # Log Transaction
            Transaction.objects.create(
                wallet=wallet, toll=instance, collector=request.user, transaction_type='DEBIT',
                status='PAID',amount=vehicle.category.toll_fee,
                reference_code=secrets.token_hex(10)
            )
            # serializer = self.get_serializer(instance)
            # headers = self.get_success_headers(serializer.data)
            return Response({"results": "Payment Successful"}, status=status.HTTP_200_OK)


class AdminTollViewSet(ModelViewSet):
    model = Toll
    serializer_class = TollSerializer
    permission_classes = [IsAdminUser]
    queryset = Toll.objects.all()


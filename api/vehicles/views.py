from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser
)
from rest_framework.decorators import action

# django imports
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from api.users.permissions import IsCollector, IsUser
from api.users.models import User
from .models import VehicleType
from .serializers import VehicleTypeSerializer


class VehicleTypeViewSet(ReadOnlyModelViewSet):
    model = VehicleType
    serializer_class = VehicleTypeSerializer
    permission_classes = [AllowAny]
    queryset = VehicleType.objects.filter(active=True)


class AdminVehicleTypeViewSet(ModelViewSet):
    model = VehicleType
    serializer_classs = VehicleTypeSerializer
    permission_classes = [IsAdminUser]
    queryset = VehicleType.objects.all()


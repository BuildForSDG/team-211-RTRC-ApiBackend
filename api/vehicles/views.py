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
from .models import VehicleCategory, Vehicle
from .serializers import VehicleCategorySerializer, VehicleSerializer


class VehicleCategoryViewSet(ReadOnlyModelViewSet):
    model = VehicleCategory
    serializer_class = VehicleCategorySerializer
    permission_classes = [AllowAny]
    queryset = VehicleCategory.objects.filter(active=True)


class AdminVehicleCategoryViewSet(ModelViewSet):
    model = VehicleCategory
    serializer_class = VehicleCategorySerializer
    permission_classes = [IsAdminUser]
    queryset = VehicleCategory.objects.all()


class VehicleViewSet(ModelViewSet):
    model = Vehicle
    serializer_class = VehicleSerializer
    permission_classes = [IsUser, IsCollector]

    def get_queryset(self):
        if self.request.user.is_collector:
            return Vehicle.objects.all()
        elif self.request.user.is_user:
            return Vehicle.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        category = VehicleCategory.objects.get(id=request.data['category'])
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, category=category)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        category = VehicleCategory.objects.get(id=request.data['category'])
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(category=category)
        headers=self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK, headers=headers)


class AdminVehicleViewSet(ModelViewSet):
    model = Vehicle
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminUser]
    queryset = Vehicle.objects.all()

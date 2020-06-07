from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)
# from rest_framework.decorators import action

# django imports
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
from api.users.permissions import IsCollector, IsUser
# from api.users.models import User
from .models import VehicleCategory, Vehicle
from .serializers import VehicleCategorySerializer, VehicleSerializer
import qrcode
import io
from cloudinary import uploader


class VehicleCategoryViewSet(ReadOnlyModelViewSet):
    model = VehicleCategory
    serializer_class = VehicleCategorySerializer
    permission_classes = [IsUser, IsCollector]
    queryset = VehicleCategory.objects.filter(active=True)


class AdminVehicleCategoryViewSet(ModelViewSet):
    model = VehicleCategory
    serializer_class = VehicleCategorySerializer
    permission_classes = [IsAdminUser]
    queryset = VehicleCategory.objects.all()

    def create(self, request, *args, **kwargs):
        # upload image
        uploaded_file = uploader.upload(request.data['image'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(image=uploaded_file['secure_url'])
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # upload image
        # uploaded_file = uploader.upload(request.data['image'])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VehicleViewSet(ModelViewSet):
    model = Vehicle
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_user:
            return Vehicle.objects.filter(user=self.request.user)
        elif self.request.user.is_collector or self.request.user.is_staff:
            return Vehicle.objects.all()

    def create(self, request, *args, **kwargs):
        category = VehicleCategory.objects.get(id=request.data['category'])
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, category=category)
        # generate qr_code, upload and save URL.
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=2)
        qr.add_data(serializer.data['id'])
        img = qr.make_image()
        imgByte = io.BytesIO()
        img.save(imgByte, format='PNG')
        final_image = imgByte.getvalue()
        uploaded_file = uploader.upload(final_image)
        instance = self.model.objects.get(id=serializer.data['id'])
        instance.qr_code = uploaded_file['secure_url']
        instance.save()
        serializer = self.get_serializer(instance)

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

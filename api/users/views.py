# drf imports
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser
)
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_auth.registration.serializers import VerifyEmailSerializer
from allauth.account.views import ConfirmEmailView

# django imports
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# apps imports
from .serializers import (
    UserSerializer,
    AdminUserSerializer,
    NationalIdTypeSerializer,
    CollectorSerializer
)

from .models import User, NationalIdType
from config.sytem_vars import DEFAULT_ADMIN_PASSWORD
from .permissions import IsCollector, IsUser


class NationalIdTypeViewSet(ReadOnlyModelViewSet):
    model = NationalIdType
    serializer_class = NationalIdTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = NationalIdType.objects.all()


class AdminNationalIdTypeViewSet(ModelViewSet):
    model = NationalIdType
    serializer_class = NationalIdTypeSerializer
    permission_classes = [IsAdminUser]
    queryset = NationalIdType.objects.all()


class CollectorViewSet(ReadOnlyModelViewSet):
    model = User
    permission_classes = [IsCollector]
    serializer_class = CollectorSerializer

    def get_queryset(self):
        return self.model.objects.filter(id=self.request.user.id)


class AdminCollectorViewSet(ModelViewSet):
    model = User
    permission_classes = [IsAdminUser]
    serializer_class = CollectorSerializer
    queryset = User.objects.filter(is_collector=True)

    def create(self, request, *args, **kwargs):
        id_type = NationalIdType.objects.get(id=request.data['national_id_type'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(national_id_type=id_type)

        # set default password
        new_user = User.objects.get(id=serializer.data['id'])
        new_user.is_collector = True
        new_user.set_password(DEFAULT_ADMIN_PASSWORD)
        new_user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        id_type = NationalIdType.objects.get(id=request.data['national_id_type'])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(national_id_type=id_type)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class UserViewSet(ModelViewSet):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        return Response({'detail':'Not Alloed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({'detail':'Not Alloed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AdminUserViewSet(ModelViewSet):
    model = User
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()


@api_view
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView, ConfirmEmailView):
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)

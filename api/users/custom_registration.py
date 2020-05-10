from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import get_username_max_length
from allauth.account import app_settings as allauth_settings
from rest_framework import serializers
import secrets
from api.wallet.models import Wallet


class CustomRegistrationSerializer(RegisterSerializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=True
    )
    email = serializers.EmailField(required=True, write_only=True)
    phone = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=True)
    password1 = serializers.CharField(write_only=True, required=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'name': self.validated_data.get('name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.phone = self.validated_data.get('phone', '')
        user.name = self.validated_data.get('name', '')
        user.save()

        user.is_user = True
        user.save()

        # Create Wallet for user
        Wallet.objects.create(user=user, balance=0.00, currency='GHC', name='Core Wallet')

        return user

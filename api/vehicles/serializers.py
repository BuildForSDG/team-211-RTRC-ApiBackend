from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import VehicleType
from api.users.serializers import UserSerializer
from api.users.models import User


class VehicleTypeSerializer(ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'


from rest_framework.serializers import ModelSerializer

from .models import VehicleCategory, Vehicle
from api.users.serializers import UserSerializer


class VehicleCategorySerializer(ModelSerializer):
    class Meta:
        model = VehicleCategory
        fields = '__all__'
        read_only_fields = ('id', 'image',)


class VehicleSerializer(ModelSerializer):
    category = VehicleCategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'user', 'license_number', 'registration_number', 'model',
            'category', 'chassis_number', 'qr_code',
            'created_at', 'updated_at',
        ]
        read_only_fields = ('id',)
    



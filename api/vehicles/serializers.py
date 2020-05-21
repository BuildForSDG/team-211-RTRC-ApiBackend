from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import VehicleCategory, Vehicle
from api.users.serializers import UserSerializer
from api.users.models import User
import pyqrcode
from pyqrcode import QRCode


class VehicleCategorySerializer(ModelSerializer):
    class Meta:
        model = VehicleCategory
        fields = '__all__'


class VehicleSerializer(ModelSerializer):
    category = VehicleCategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    # qr_code_image = SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            'id', 'user', 'license_number', 'registration_number', 'model',
            'category', 'chassis_number',
            'created_at', 'updated_at',
        ]
        read_only_fields = ('id',)
    
    # def get_qr_code_image(self, obj):
    #     obj.qr_code.png('qr-code.png', scale=8)



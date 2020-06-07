from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import VehicleCategory, Vehicle
from api.users.serializers import UserSerializer
from api.wallet.models import Wallet


class VehicleCategorySerializer(ModelSerializer):
    class Meta:
        model = VehicleCategory
        fields = '__all__'
        read_only_fields = ('id', 'image',)


class VehicleSerializer(ModelSerializer):
    category = VehicleCategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    sufficient_funds = SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            'id', 'user', 'license_number', 'registration_number', 'model',
            'category', 'chassis_number', 'qr_code', 'sufficient_funds',
            'created_at', 'updated_at',
        ]
        read_only_fields = ('id',)
    
    def get_sufficient_funds(self, obj):
        toll_fee = obj.category.toll_fee
        wallet = Wallet.objects.get(user=obj.user)
        wallet_funds = wallet.balance

        if wallet_funds > toll_fee:
            return True
        else:
            return False




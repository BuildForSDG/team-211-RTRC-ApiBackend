from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import (
    TollLocation,
    Toll,
)
from api.users.serializers import UserSerializer
from api.users.models import User
from api.vehicles.serializers import VehicleSerializer


class TollLocationSerializer(ModelSerializer):
    collectors = SerializerMethodField()

    class Meta:
        model = TollLocation
        fields = '__all__'

    def get_collectors(self, obj):
        if self.request.user.is_user:
            collectors = None
        else:
            collectors = obj.collectors.all()
        return UserSerializer(collectors, many=True).data


class TollSerializer(ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    collector = UserSerializer(read_only=True)

    class Meta:
        model = Toll
        fields = [
            'id', 'vehicle', 'collector', 'status', 'paid_on', 'reference',
            'created_at', 'updated_at'
        ]
        read_only_fields = (
            'id', 'status', 'paid_on', 'reference'
        )

from rest_framework.serializers import (
    ModelSerializer, 
    SerializerMethodField, 
    PrimaryKeyRelatedField,
)
from rest_framework import serializers

from .models import User, NationalIdType


class NationalIdTypeSerializer(ModelSerializer):
    class Meta:
        model = NationalIdType
        fields = '__all__'


class CollectorSerializer(ModelSerializer):
    national_id_type = NationalIdTypeSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'is_collector', 'name',
            'national_id', 'national_id_type', 'digital_address'
            ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'name',
            'phone',
            'is_user',
            'is_collector',
        ]
        read_only_fields = (
            'id',
            'email',
            'username',
            'is_user',
            'is_collector',
        )


class AdminUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'username',
            'phone',
            'is_staff',
        ]
        read_only_fields = (
            'id',
            'email',
            'username',
            'is_staff',
        )


class UserDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk',
                  'name',
                  'date_joined',
                  'is_active',
                  'email',
                  'username',
                  'phone',
                  'is_staff',
                  'is_collector',
                  'is_user'
                  ]


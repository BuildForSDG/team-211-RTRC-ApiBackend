from django.db import models
from django.conf import settings
import uuid


class VehicleCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, unique=True)
    toll_fee = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    image = models.URLField(null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} - {1} - {2}".format(str(self.name), str(self.toll_fee), str(self.id))


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    license_number = models.CharField(max_length=250)
    registration_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=250)
    category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, related_name='vehicle_categories')
    chassis_number = models.CharField(max_length=250, unique=True)
    qr_code = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.registration_number)


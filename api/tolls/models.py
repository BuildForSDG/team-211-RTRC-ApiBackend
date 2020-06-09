from django.db import models
from django.conf import settings
import uuid
import api.tolls.contants as const
from api.vehicles.models import Vehicle


class TollLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, unique=True)
    address = models.CharField(max_length=250, unique=True)
    active = models.BooleanField(default=False)
    collectors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collectors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} - {1}" .format(str(self.name), str(self.address))


class Toll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='vehicle_tolls')
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='collector_tolls')
    location = models.ForeignKey(TollLocation, on_delete=models.SET_NULL, null=True, related_name='toll_locations')
    status = models.CharField(max_length=10, choices=const.TOLL_STATUS_CHOICES, default=const.UNPAID)
    paid_on = models.DateTimeField(null=True)
    reference = models.CharField(max_length=50, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} - {1}".format(str(self.vehicle.user.username), str(self.location.name))


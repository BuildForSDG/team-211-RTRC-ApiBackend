from django.db import models
from django.conf import settings
import uuid
import secrets
import random
from hashids import Hashids
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
        return str(self.name)


class Toll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='vehicle_tolls')
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='collector_tolls')
    status = models.CharField(max_length=10, choices=const.TOLL_STATUS_CHOICES, default=const.UNPAID)
    paid_on = models.DateTimeField(null=True)
    reference = models.CharField(max_length=50, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.reference)

    def generate_hashid(self):
        hash_ids = Hashids(
            salt='E-Revenue',
            min_length=8
        )
        hash_id = hash_ids.encode(random.randint(1, 10000000))
        return hash_id.upper()

    def get_key(self):
        reference = self.generate_hashid()
        while Toll.objects.filter(reference=reference).exists():
            reference = self.generate_hashid()
        self.reference = reference
        self.save()

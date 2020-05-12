from django.test import TestCase
from .models import VehicleType


class TestVehicles(TestCase):
    def setUp(self):
        VehicleType.objects.create(
            name='TRO TRO',
            toll_fee=1.00,
            active=True
        )

    def test_models(self):
        v_type = VehicleType.objects.get(name='TRO TRO')
        self.assertEqual(v_type.name, 'TRO TRO')

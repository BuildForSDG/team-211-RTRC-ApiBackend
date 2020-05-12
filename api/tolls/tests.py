from django.test import TestCase
from .models import TollLocation
from api.users.models import User


class TestTolls(TestCase):
    def setUp(self):
        TollLocation.objects.create(
            name='Anomabo Toll Booth',
            address='Ano-2x5-223',
            active=True
        )
    
    def test_models(self):
        toll = TollLocation.objects.get(name='Anomabo Toll Booth')
        self.assertEqual(toll.name, 'Anomabo Toll Booth')


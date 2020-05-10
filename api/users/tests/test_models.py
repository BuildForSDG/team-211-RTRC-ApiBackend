from django.test import TestCase
from ..models import User


class UserTest(TestCase):

    def setUp(self):
        new_user = User(username='tester', email='metesteremail@gmail.com', password='dynamo0000')
        new_user.set_password('dynamo0000')
        new_user.save()

    def test_user(self):
        user = User.objects.get(username='tester')
        self.assertEqual(user.username, 'tester')

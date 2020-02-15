from django.contrib.auth.models import User
from django.test import TestCase
from main.models import Abonnement, AbonnementType


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(email='test@test.be', password='123456')  # noqa: S106
        Abonnement.objects.create(package=AbonnementType.package1, user=user)

    def test_user_has_sub(self):
        """Animals that can speak are correctly identified"""
        user = User.objects.get(email='test@test.be')
        sub = Abonnement.objects.filter(user=user)
        self.assertIsNotNone(sub)

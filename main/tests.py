from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.utils import timezone

from main.models import Package, Subscription, User


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(email='test@test.be', password='123456')  # noqa: S106
        package = Package.objects.create(price=1.0, period=timedelta(hours=1), name='Package1', description='')
        Subscription.objects.create(package=package, user=user, started_at=timezone.now())

    def tearDown(self):
        user = User.objects.get(email='test@test.be')
        user.delete()

    def test_user_has_sub(self):
        """Animals that can speak are correctly identified"""
        user = User.objects.get(email='test@test.be')
        sub = get_object_or_404(Subscription.objects, user=user)
        self.assertIsNotNone(sub)
        self.assertTrue(user.is_subscribed)

from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubcriptionModelTest(TestCase):

    def setUp(self) -> None:
        self.obj = Subscription(
            name='Andressa Monteiro',
            cpf='12345678901',
            email='andressamonteiro@gmail.com',
            phone='11-99999-8888'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Andressa Monteiro', str(self.obj))

    def test_paid_default_to_False(self):
        """By defalut paid must be False"""
        self.assertEqual(False, self.obj.paid)

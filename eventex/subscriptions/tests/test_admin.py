from unittest.mock import Mock

from django.test import TestCase
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin


class SubscriptionModelAdminTest(TestCase):

    def setUp(self) -> None:
        Subscription.objects.create(name='Fernando Meireles', cpf='12345678901',
                                    email='fernando@meireles.com', phone='11-99999-8888'
                                    )

        # instancio o SubscritionModelAdmin
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)

    def test_has_action(self):
        """Action mark as paid should be installed"""
        self.assertIn('mark_as_paid', self.model_admin.actions)

    def test_mark_all(self):
        """It should mark all selected subscriptions as paid"""
        self.call_action()

        self.assertEqual(1, Subscription.objects.filter(paid=True).count())

    def test_message(self):
        """It should send a message to the user."""

        mock = self.call_action()
        mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')

    def call_action(self):
        # montar a query
        query_set = Subscription.objects.all()

        # Mock
        mock = Mock()
        old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock

        # chamar a action
        self.model_admin.mark_as_paid(None, query_set)

        SubscriptionModelAdmin.message_user = old_message_user

        return mock



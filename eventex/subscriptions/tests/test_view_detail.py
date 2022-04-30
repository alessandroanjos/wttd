from django.test import TestCase
from django.shortcuts import resolve_url as resolve

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):

    def setUp(self) -> None:
        self.obj = Subscription.objects.create(
            name='Fernando Meireles',
            cpf='12345678901',
            email='fernando@email.com',
            phone='11-99999-8888',
            created_at='2022-04-29'
        )
        # self.response = self.client.get('/inscricao/{}/'.format(self.obj.pk))
        self.response = self.client.get(resolve('subscriptions:detail', self.obj.pk))


    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.response.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = (self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.response, expected)


class SubscriptionDetailNotFound(TestCase):

    def test_not_found(self):
        # response = self.client.get('inscricao/0/')
        response = self.client.get(resolve('subscriptions:detail', 0))

        self.assertEqual(404, response.status_code)
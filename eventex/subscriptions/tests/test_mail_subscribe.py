from django.test import TestCase
from django.core import mail
from django.test.utils import override_settings


class SubscribePostValid(TestCase):

    @override_settings(DEBUG=True)
    def setUp(self) -> None:
        data = dict(name='Fernando Meireles', cpf='12345678901',
                    email='fernando@meireles.com', phone='11-99999-8888')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]


    def test_subscription_email_subject(self):
        expect = 'Confirmacao de Inscricao'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'fernando@meireles.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Fernando Meireles',
            '12345678901',
            'fernando@meireles.com',
            '11-99999-8888',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscribe_form_template.html """
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """Html must constain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


    def test_has_form(self):
        """Context must have subcription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):

    def setUp(self) -> None:
        data = dict(name='Fernando Meireles', cpf='12345678901',
                    email='fernando@meireles.com', phone='11-99999-8888')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """ Valid POST should redirect to /inscricao/ """
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmacao de Inscricao'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'fernando@meireles.com']
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Fernando Meireles', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('fernando@meireles.com', email.body)
        self.assertIn('11-99999-8888', email.body)


class SubcribeInvalidPost(TestCase):

    def setUp(self) -> None:
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_forms_has_erros(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)


class SubcribeSuccessMessage(TestCase):

    def test_message(self):
        data = dict(name='Fernando Meireles', cpf='12345678901',
                    email='fernando@email.com', phone='11-99999-8888')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
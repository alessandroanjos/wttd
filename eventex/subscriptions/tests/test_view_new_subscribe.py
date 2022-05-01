from django.test.utils import override_settings
from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as resolve

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get(resolve('subscriptions:new'))

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscribe_form_template.html """
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""

        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1),
                )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """Html must constain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subcription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    # Teste refatorado em test_form_subscription.py
    # def test_form_has_fields(self):
    #     """Form must have 4 fields"""
    #     form = self.response.context['form']
    #     self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscriptionsNewPostValid(TestCase):

    @override_settings(DEBUG=True)
    def setUp(self) -> None:
        data = dict(name='Fernando Meireles', cpf='45481811057',
                    email='fernando@meireles.com', phone='11-99999-8888')
        self.response = self.client.post(resolve('subscriptions:new'), data)

    def test_post(self):
        """ Valid POST should redirect to /inscricao/1/ """
        self.assertRedirects(self.response, resolve('subscriptions:detail', 1))
        # self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):

    def setUp(self) -> None:
        self.response = self.client.post(resolve('subscriptions:new'), {})

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

    def test_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())

# @unittest.skip('To be removed')
# class SubcribeSuccessMessage(TestCase):
#
#     def test_message(self):
#         data = dict(name='Fernando Meireles', cpf='12345678901',
#                     email='fernando@email.com', phone='11-99999-8888')
#
#         response = self.client.post('/inscricao/', data, follow=True)
#         self.assertContains(response, 'Inscrição realizada com sucesso!')


class TemplateRegressionTest(TestCase):

    def test_template_has_non_field_errors(self):
        invalid_data = dict(name='Fernando Meireles', cpf='45481811057')
        response = self.client.post(resolve('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield">')
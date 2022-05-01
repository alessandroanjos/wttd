from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        self.form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_cpf_is_digits(self):
        """CPF must only accept digits."""
        form = self.make_validated_form(cpf='ABC45678901')
        # form.erros é um dict que cada chave é o nome do campo que contem erro.
        # O valor de cada chave é uma lista com os erros

        # self.assertListEqual(['cpf'], list(form.errors))
        self.assertFormErrorsMessage(form, 'cpf', 'CPF deve conter apenas números')

        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_has_11_digits(self):
        """CPF must have 11 digits"""
        form = self.make_validated_form(cpf='1234')
        # self.assertListEqual(['cpf'], list(form.errors))
        msg = 'CPF deve ter 11 números'
        field = 'cpf'

        self.assertFormErrorsMessage(form, field, msg)

        field = 'cpf'
        code = 'length'
        self.assertFormErrorCode(form, field, code)

    def test_cpf_is_invalid(self):
        pass
        # CPF must only accepts digits
        form = self.make_validated_form(cpf='01234567891')
        self.assertListEqual(['cpf'], list(form.errors))

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorsMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Fernando Meireles', cpf='12345678901',
                     email='fernando@meireles.com', phone='11-99999-8888')
        data = dict(valid, **kwargs)
        # instancia o formulario
        form = SubscriptionForm(data)
        # ativar a validacao
        form.is_valid()
        return form

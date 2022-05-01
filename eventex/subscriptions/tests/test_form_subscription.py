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
        """CPF must only accepts valid value"""
        form = self.make_validated_form(cpf='12345678901')
        self.assertListEqual(['cpf'], list(form.errors))

    def test_name_must_be_capitalized(self):
        """Name must be capitalized"""
        # FERNANDO MEIRELES -> Fernando Meireles
        form = self.make_validated_form(name='FERNANDO MEIRELES')
        self.assertEqual('Fernando Meireles', form.cleaned_data['name'])

    def test_email_is_optional(self):
        """Email is optional"""
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """Phone is optional"""
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_phone_or_email(self):
        """Email and Phone are optional, but one must be informed"""
        form = self.make_validated_form(email='', phone='')
        self.assertListEqual(['__all__'], list(form.errors))

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
        valid = dict(name='Fernando Meireles', cpf='45481811057',
                     email='fernando@meireles.com', phone='11-99999-8888')
        data = dict(valid, **kwargs)
        # instancia o formulario
        form = SubscriptionForm(data)
        # ativar a validacao
        form.is_valid()
        return form

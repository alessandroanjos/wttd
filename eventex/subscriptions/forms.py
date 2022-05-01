from django import forms
from django.core.exceptions import ValidationError
from validate_docbr import CPF


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números', 'digits')

    if len(value) != 11:
        raise ValidationError('CPF deve ter 11 números', 'length')

    cpf_br = CPF()
    if not cpf_br.validate(str(value)):
        raise ValidationError('CPF inválido', code='valida_cpf')


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validate_cpf])
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Telefone')
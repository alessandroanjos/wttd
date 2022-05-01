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

    def clean_name(self):
        name = self.cleaned_data['name']

        words = []

        # usando um set
        prep = {'da', 'das', 'de', 'do', 'dos'}

        # usando uma list
        prep = ['da', 'das', 'de', 'do', 'dos']

        for w in name.split():
            if w not in prep:
                words.append(w.capitalize())

        capitalized_name = ' '.join(words)

        # words = [w.capitalize() for w in name.split()]
        # words = [w.capitalize() if w not in prep else w for w in name.split()]
        # words = (w.capitalize() if w not in prep else w for w in name.split())

        return capitalized_name

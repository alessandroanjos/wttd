from django.contrib import messages
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':

        form = SubscriptionForm(request.POST)
        # transformar os dados que vem inv;alidos e nao checados- pega cada dado e passar
        # pelos fitlros e resultar num dicionario de dados sanitarizado

        if form.is_valid():
            """"
            context = dict(name='Fernando Meireles', cpf='12345678901',
                           email='fernando@meireles.com', phone='11-99999-8888')
            """

            body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)

            mail.send_mail('Confirmacao de Inscricao', body,
                           'contato@eventex.com.br', ['contato@eventex.com.br', form.cleaned_data['email']])

            messages.success(request, 'Inscrição realizada com sucesso!')

            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html', {'form': form})

    else:
        context = { 'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)
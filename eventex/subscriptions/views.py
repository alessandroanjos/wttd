from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as resolve
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def empty_form(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    if settings.DEBUG:
        # Send Mail
        template_name = 'subscriptions/subscription_email.txt'
        subject = 'Confirmacao de Inscricao'
        from_ = settings.DEFAULT_FROM_EMAIL
        # outra forma de fazer -> # to = form.cleaned_data['email']
        to = subscription.email
        context = {'subscription': subscription}
        _send_mail(subject, from_, to, template_name, context)

    # Success Feedback
    # messages.success(request, 'Inscrição realizada com sucesso!')

    #return HttpResponseRedirect('/inscricao/{}/'.format(subscription.pk))
    return HttpResponseRedirect(resolve('subscriptions:detail', subscription.pk))





def detail(request, pk):

    try:
        subscription = Subscription.objects.get(pk=pk)
        context = {'subscription': subscription}
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html', context)


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])

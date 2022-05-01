from django.contrib import admin
from django.utils.timezone import now

from eventex.subscriptions.models import Subscription


class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'cpf', 'created_at', 'subscribe_today', 'paid')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'email', 'phone', 'cpf')
    list_filter = ('paid', 'created_at')

    actions = ['mark_as_paid']

    def subscribe_today(self, obj):
        return obj.created_at == now().date

    subscribe_today.short_description = 'inscrito hoje?'
    subscribe_today.boolean = True

    def mark_as_paid(self, request, query_set):
        count = query_set.update(paid=True)

        if count == 1:
            msg = '{} inscrição foi marcada como paga.'
        else:
            msg = '{} inscrições foram marcadas como pagas.'

        self.message_user(request, msg.format(count))

    mark_as_paid.short_description = 'Marcar como pago'


admin.site.register(Subscription, SubscriptionModelAdmin)

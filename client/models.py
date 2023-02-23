"""A client

A client application for django.

Classes
=======

Client: The actual client.

"""
from functools import reduce

from django.db import models
from django.urls import reverse
import django.utils.timezone as tz
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.loader import render_to_string


from address.models import Address
import orders.models
# from orders.models import DeliveryAddress
from agenda.models import CurrentEvent

from roce.helpers import as_choice_tuple


class Client(models.Model):
    title = models.CharField(
        # Translators: How to address the client; mss, mr, ...
        _('title'),
        max_length=15,
        null=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name=_('client'),
        primary_key=True,
    )
    telephone = models.CharField(
        _('phone number'),
        max_length=22,
        null=True,
        blank=True,
    )
    address = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        related_name=_('client'),
        null=True,
        blank=True
    )
    delivery_address = models.ManyToManyField(
        orders.models.DeliveryAddress,
        related_name=_('client'),
        blank=True,
    )
    consumer = models.BooleanField(
        _('end consumer'),
        default=True,
    )
    vat_liable = models.BooleanField(
        _('VAT liable'),
        default=False,
    )

    class Meta:
        permissions = (
            ('user_is_client', 'Check if user is  a client'),
        )
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    def __str__(self):
        show = (self.user.first_name, self.user.last_name, self.user.username)
        return '{} {} ({})'.format(*show)

    def delivery_address_list(self):
        return self.delivery_address.all()

    def get_absolute_url(self):
        return reverse('client.views.detail')

    def full_name(self):
        show = (self.title or '',
                self.user.first_name, self.user.last_name)
        return '{} {} {}'.format(*show).strip()

    def deliveries(self):
        '''Return a Query-Set with all valid deliveries for this client.'''
        return orders.models.DeliveryDateForDeliveryAddress.objects.filter(
            start_date__gt=(
                tz.now().date() + models.F(
                    'delivery_address__order_date_limit')),
            delivery_address__client__user__id=self.user.id)

    def deliveries_choice_tuple(self):
        """Return a tuple with valid deliveries for this client."""
        def text_function(event):
            address_name = event.delivery_address.address.address_name
            event_start = tz.make_naive(event.safe_start_datetime)
            return f"{address_name}: {event_start}"
        return as_choice_tuple(self.deliveries(), text_fun=text_function)

    def payed_items(self, show_expired=False):
        order_lines = orders.models.OrderLine.objects.filter(
            order__client=self, payed=True)
        if show_expired:
            return order_lines
        return order_lines.filter(start_date__gte=tz.now().date())

    def payed_items_on_date(self, date):
        return self.payed_items(show_expired=True).filter(
            start_date__exact=date)

    def payed_items_today(self):
        return self.payed_items_on_date(tz.now().date())

    def payed_items_tomorrow(self):
        tomorrow = tz.now().date() + tz.timedelta(days=1)
        return self.payed_items_on_date(tomorrow)

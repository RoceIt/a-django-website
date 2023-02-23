import logging

from collections import defaultdict

from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone as tz
from django.utils.translation import ugettext_lazy as _

#from client.models import Client
from address.models import Address
from agenda.models import BaseEvent, CurrentEvent


class UnboundException(Exception):
    pass


logger = logging.getLogger(__name__)


class OrderItem(models.Model):
    online_price = models.DecimalField(
        _('online price'),
        max_digits=10,
        decimal_places=2,
    )

    vat_rate = models.DecimalField(
        'VAR rate',
        max_digits=6,
        decimal_places=2,
        help_text='percentage, e.g. 21',
    )

    # price_events = models.ManyToManyField(
    #     CurrentEvent,
    #     related_name='OrderItemPrice',
    # )

    # keyword_events = models.ManyToManyField(
    #     CurrentEvent,
    #     related_name='OrderItemKeyword'
    # )

    listview_order = models.PositiveSmallIntegerField(
        'listview order',
        help_text='Low numbers are shown first in the list views.',
        default=100,
        )

    listview_show = models.BooleanField(
        'show in listview',
        help_text='Uncheck when article should not be displayed.',
        default=True,
    )

    def __str__(self):
        try:
            output_str = self.product.name
        except FieldDoesNotExist:
            output_str = 'Unbound OrderItem'
        return output_str

    @property
    def _product_field_name(self):
        for name in self.__dir__():
            if name.startswith('product_'):
                return name

    @property
    def product(self):
        for name in self.__dir__():
            if name.startswith('product_'):
                try:
                    # print('returning: ', name)
                    return self.__getattribute__(name)
                except Exception as e:
                    print('maybe doing something dangerous now, '
                          ' orders.models.py')
                    raise FieldDoesNotExist
        raise FieldDoesNotExist

    def carry_out_active_price_change(self):
        for change in self.pricechangeondate_set.filter(
                start_date__lte=tz.now().date()).order_by(
                    'start_date'):
            if change.new_price is not None:
                self.online_price = change.new_price
                logger.info(
                    f'changed price {self.product.name} to {change.new_price}')
            if change.new_vat is not None:
                self.vat_rate = change.new_vat
                logger.info(
                    f'changed vat {self.product.name} to {change.new_vat}')
            self.save()
            change.delete()
            logger.info('removed pricechang {change}')

    def check_for_assembly_point_promotion_price(
            self, client, assembly_point, delivery_date, current_price):
        """
        Checks for a promotion price and return it if lower then the
        current price given.
        """
        promotions = self.assemblypointpromotion_set.filter(
            assemblypoint__id=assembly_point.id)
        for promo in promotions.all():
            if promo.expired():
                promo.delete()
            elif delivery_date in promo:
                current_price = min(current_price, promo.promotion_price)
        return current_price

    def price(self, client=None, assembly_point=None, delivery_date=None):
        self.carry_out_active_price_change()
        current_price = self.online_price
        if assembly_point is not None and delivery_date is not None:
            current_price = self.check_for_assembly_point_promotion_price(
                client, assembly_point, delivery_date, current_price)
        print(client)
        if client and client.vat_liable:
            current_price /= (1 + self.vat_rate/100)
        return current_price

    @classmethod
    def as_id_name_choices_tuple(cls):
        return sorted(
            [(item.id, item.product.name) for item in cls.objects.all()],
            key=lambda x: x[1]
        )


class DeliveryAddress(models.Model):
    """An address to deliver to.

    Model with an address and a type. For now.
    """

    FREE = 'FR'
    NONE = 'NO'
    ASSEMBLY_POINT = 'AP'

    KIND_OF_DELIVERY_CHOICES = (
        (FREE, _('Free')),
        (NONE, _('None')),
        (ASSEMBLY_POINT, _('Assambly point'))
    )

    ORDER_DELTAS = ((tz.timedelta(days=0), _('no restrictions')),
                    (tz.timedelta(days=1), _('1 day')),
                    (tz.timedelta(days=2), _('2 days')))

    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
    )

    kind = models.CharField(
        _('type'),
        max_length=2,
        choices=KIND_OF_DELIVERY_CHOICES,
        default=NONE,
    )

    order_date_limit = models.DurationField(
        _('orders accepted until'),
        choices=ORDER_DELTAS,
        default=tz.timedelta(days=2))

    show_in_client_options_p = models.BooleanField(
        _('show in client\'s delivery address options'),
        default=False,
    )

    def __str__(self):
        return (f'Delivery ({self.get_kind_display()}): '
                f'{self.address.address_name}')

    @property
    def unique_id_str(self):
        return f"[{self.id}]{str(self)}"


class DeliveryDateForDeliveryAddress(BaseEvent):

    delivery_address = models.ForeignKey(
        DeliveryAddress,
        verbose_name=_('delivery address'),
        related_name='deliveries'
    )

    def __str__(self):
        return f'{self.start_date}: {self.delivery_address.address.name}'


class PriceChangeOnDate(BaseEvent):

    order_item = models.ForeignKey(
        OrderItem,
        verbose_name=_('order item'),
    )

    new_price = models.DecimalField(
        _('new price'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    new_vat = models.DecimalField(
        _('new VAT rate'),
        max_digits=6,
        decimal_places=2,
        help_text='percentage, e.g. 21',
        blank=True,
        null=True,
    )

    def __str__(self):
        return (f'{self.order_item.product.name} '
                f'{self.safe_start_date}')


class AssemblyPointPromotion(BaseEvent):

    order_item = models.ForeignKey(
        OrderItem,
        verbose_name=_('Promotion product'),
    )

    assemblypoint = models.ManyToManyField(
        DeliveryAddress,
        limit_choices_to={'kind': DeliveryAddress.ASSEMBLY_POINT},
        verbose_name=_('assembly point'),
    )

    promotion_price = models.DecimalField(
        _('promotion price'),
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return (f'{self.order_item.product.name} assembly point promotion '
                f'({self.safe_start_date} / {self.safe_end_date})')

    def __contains__(self, date):
        datetime = tz.make_aware(tz.datetime(date.year, date.month, date.day))
        return super().__contains__(datetime)

    def expired(self):
        return tz.now().date() > self.safe_end_date


class Order(BaseEvent):

    NEW_ORDER = 1
    PAYMENT_PENDING = 2
    PAYED = 3

    # state = models.SmallIntegerField(
    #     _('state'),
    # ),

    client = models.ForeignKey(
        'client.Client',
        # client.models.Client,
        blank=True,
        null=True,
    )

    state = models.SmallIntegerField(
        _('state'),
        default=NEW_ORDER,
    )

    payment_service = models.CharField(
        max_length=20,
        blank=True
    )

    payment_id = models.CharField(
        max_length=50,
        blank=True,
    )

    def __str__(self):
        name = f'{self.client.user.first_name} {self.client.user.last_name}'
        return f'{self.start_date} {name} ({len(self)})'

    def __len__(self):
        """Returns the number of orderlines in the order.

         Maybe better to return the number of items?
        """
        return self.orderline_set.count()

    def nr_of_deposits(self):
        return self.deposit_set.count()

    def orderitem_total(self):
        return self.orderline_set.aggregate(models.Sum('price'))['price__sum']

    def deposit_total(self):
        return self.deposit_set.aggregate(models.Sum('value'))['value__sum']

    def deposit_refund(self):
        return self.client.deposit_set.filter(
            returned=True, refunded=False).aggregate(
                models.Sum('value'))['value__sum']

    def total(self):
        total = self.orderitem_total() + self.deposit_total()
        refund = self.deposit_refund()
        if refund is not None:
            total -= refund
        return total

    def interrupted(self):
        return self.state == self.NEW_ORDER

    def as_table(self):
        return self.orderlines_as_table(self.orderline_set.all())
        # return render_to_string('orders/order_lines.html',
        #                         {'order': self.orderline_set.all()})

    @staticmethod
    def orderlines_as_table(orderlines):
        return render_to_string('orders/order_lines.html',
                                {'orderlines': orderlines})

    def as_category_table(self):
        return self.orderlines_as_category_table(self.orderline_set.all())
        # cat_order = defaultdict(list)
        # for orderline in self.orderline_set.all():
        #     cat_order[orderline.category].append(orderline)
        # return render_to_string('orders/categorized_order_lines.html',
        #                         {'cat_order': dict(cat_order)})

    @classmethod
    def orderlines_as_category_table(cls, orderlines):
        cat_order = defaultdict(list)
        for orderline in orderlines:
            cat_order[orderline.category].append(orderline)
        return render_to_string('orders/categorized_order_lines.html',
                                {'cat_order': dict(cat_order)})


    def payment_confirmed(self, service, payment_id):
        self.state = self.PAYED
        self.payment_service = service
        self.payment_id = payment_id
        self.save()
        for orderline in self.orderline_set.all():
            orderline.payed = True
            orderline.save()


class OrderLineManager(models.Manager):

    def production_orders(self):
        return super().get_queryset().filter(
            payed=True,
            start_date__gte=tz.now().date())

    def delivery_dates(self):
        return self.production_orders().\
            values_list('start_date', flat=True).\
            order_by('start_date')

    def orders_on_date(self, date):
        return super().get_queryset().filter(
            start_date=date)


class OrderLine(BaseEvent):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )

    category = models.CharField(
        max_length=70,
    )

    number = models.PositiveSmallIntegerField(
        _('number'),
    )

    orderitem = models.ForeignKey(
        OrderItem,
        on_delete=models.PROTECT,
    )

    cart_info = models.CharField(
        max_length=200,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,)

    payed = models.BooleanField(
        _('payed'),
        default=False,
    )

    objects = OrderLineManager()

    def __str__(self):
        return self.orderitem.product.name

    # def production_orders(self):
    #     """Orders that are payed, or are marked as ok to produce, with a
    #     start date today or in the future.

    #     """
    #     return self.objects.filter(
    #         payed=True,
    #         start_date__gte=tz.now().date())



class Deposit(models.Model):
    REFUNDED = 'refunded'
    PENDING = 'pending refund'
    OUT = 'at client'

    name = models.CharField(
        _('name'),
        max_length=50,
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    returned = models.BooleanField(
        _('returned'),
        default=False,
    )

    refunded = models.BooleanField(
        _('returned'),
        default=False,
    )

    order = models.ForeignKey(
        Order,
        verbose_name=_('order'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    client = models.ForeignKey(
        'client.Client',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        )

    def __str__(self):
        status = self.status()
        return f'{self.id} {status}'

    def status(self):
        if self.refunded:
            return self.REFUNDED
        elif self.returned:
            return self.PENDING
        else:
            return self.OUT

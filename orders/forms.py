import json

from django import forms
from django.core import validators
from django.utils import timezone as tz
from django.forms import formset_factory
from django.utils.translation import ugettext_lazy as _


from .models import DeliveryAddress
import orders.models as model
# from .agenda import delivery_agenda, pricing_agenda, keyword_agenda
import orders.agenda as agenda_def

from address.models import Address
from agenda.models import CurrentEvent
from orders.models import OrderItem

import roce.helpers as helper

class AddToCartForm(forms.Form):
    product = forms.IntegerField(
        widget=forms.HiddenInput,
        # maybe add a validate?,
    )
    number = forms.IntegerField(
        label=_('number'),
        initial=1,
        min_value=1,)


class AddToCartWithDateInfo(AddToCartForm):
    delivery_date = forms.DateField(
        label=_('delivery_date'),
        initial=tz.now(),
    )


class AddToCartWithExtraRequestsInfo(AddToCartForm):
    special_requests = forms.CharField(
        label=_('special requests'),
        widget=forms.Textarea(attrs={'rows': 3,
                                     'cols': 55}),
        max_length=150,
        required=False,
        initial='',
    )


class AddToCartWithEventInfo(AddToCartForm):
    delivery_event_id = forms.ChoiceField(
        label=_('delivery'),
        choices=(),
    )

    def validate(self, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        d_event_choice_list = kwargs.pop('choice_list', None)
        super().__init__(*args, **kwargs)
        # print(d_event_choice_list)
        if d_event_choice_list:
            self.fields['delivery_event_id'].choices = d_event_choice_list


class AddToCartWithEventExtraRequestsInfo(AddToCartWithExtraRequestsInfo):
    delivery_event_id = forms.ChoiceField(
        label=_('delivery'),
        choices=(),
    )

    def validate(self, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        d_event_choice_list = kwargs.pop('choice_list', None)
        super().__init__(*args, **kwargs)
        # print(d_event_choice_list)
        if d_event_choice_list:
            self.fields['delivery_event_id'].choices = d_event_choice_list


class CartLine(forms.Form):
    number = forms.IntegerField(
        label=_('number'),
        min_value=0)
    product_id = forms.IntegerField(
        widget=forms.HiddenInput,
    )
    product_description = forms.CharField(
        label=_('product description'),
        max_length=50,
        disabled=True,
        required=True)
    info_description = forms.CharField(
        label=_('information'),
        max_length=200,
        disabled=True,
        required=True)
    price = forms.DecimalField(
        label=_('price'),
        max_digits=10,
        decimal_places=2,
        disabled=True,
        required=True)


cart_table = formset_factory(CartLine, can_delete=True, extra=0)


class DeliveryAddressForm(forms.ModelForm):
    """The basic form for the DeliveryAddress model."""

    address_name = forms.ChoiceField(
        choices=Address.as_id_name_choices_tuple,
        required=True,
        )

    field_order = ['kind', 'show_in_client_options_p']

    class Meta:
        model = DeliveryAddress
        fields = ['kind', 'show_in_client_options_p']

    def save(self, commit=True):
        new_delivery_address = super().save(commit=False)
        new_delivery_address.address = Address.objects.get(
            id=self.cleaned_data['address_name'])
        new_delivery_address.kind = self.cleaned_data['kind']
        if commit:
            new_delivery_address.save()
            return new_delivery_address

    @staticmethod
    def latest_adres_list():
        return Address.objects.values_list('id', 'name').order_by('name')


class DeliveryDateForDeliveryAddressForm(forms.ModelForm):

    field_order = ['start_date']

    class Meta:
        model = model.DeliveryDateForDeliveryAddress
        fields = ['start_date']
        labels = {
            'start_date': _('date'),
        }

    def clean_start_date(self):
        """Check if start date is today or in the future"""
        return helper.clean_date_gte(
            self, 'start_date', tz.now().date())

    def save(self, delivery_address, commit=True):
        form = super().save(commit=False)
        form.title = _('Delivery date for delivery address')
        form.delivery_address = delivery_address
        if commit:
            form.save()
        return form


class PriceChangeOnDateForm(forms.ModelForm):

    field_order = ['order_item', 'start_date', 'new_price', 'new_vat']

    class Meta:
        model = model.PriceChangeOnDate
        fields = ['order_item', 'start_date', 'new_price', 'new_vat']
        labels = {
            'start_date': _('date'),
        }

    def clean_start_date(self):
        return helper.clean_date_gte(self, 'start_date', tz.now().date())

    def clean(self):
        cleaned_data = super().clean()
        new_price = cleaned_data.get('new_price')
        new_vat = cleaned_data.get('new_vat')
        if new_price is None and new_vat is None:
            raise forms.ValidationError(
                _('new price and new VAT can\'t both be empty.'),
                code='invalid',
            )


class AssembyPointPromotionForm(forms.ModelForm):

    field_order = ['order_item', 'assemblypoint',
                   'start_date', 'end_date', 'promotion_price']

    class Meta:
        model = model.AssemblyPointPromotion
        fields = ['order_item', 'assemblypoint',
                  'start_date', 'end_date', 'promotion_price']
        labels = {
            'start_date': _('start promotion'),
            'end_date': _('end promotion'),
        }

    def clean_start_date(self):
        return helper.clean_date_gte(self, 'start_date', tz.now().date())

    def clean_end_date(self):
        return helper.clean_field_required(self, 'end_date')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(
                _('Start of promotion can\'t be after end of promotion.'),
                code='invalid',
            )


class ADate(forms.Form):

    adate = forms.DateField(
        label=_('Orders for date'),
        required=True,
    )

# class OrderItemKeyword(forms.Form):
#     """Form to set a keyword for a product.

#     This creates an event where you can set a keyword on a product
#     during a specified time.
#     """

#     orderitem_id = forms.ChoiceField(
#         choices=OrderItem.as_id_name_choices_tuple,
#         required=True,
#         )

#     start_date = forms.DateField(
#         label=_('start date'),
#         initial=tz.now().date(),
#         validators=[validators.MinValueValidator(
#             tz.now().date(),
#             _('Start date is already past, you can\'t deliver then anymore!')),
#         ],
#         required=True,
#     )

#     end_date = forms.DateField(
#         label=_('end date'),
#         required=True,
#     )

#     keyword = forms.CharField(
#         label=_('keyword'),
#         max_length=10,
#         required=True,
#     )

#     def clean(self):
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get('start_date')
#         end_date = cleaned_data.get('end_date')

#         if start_date and end_date:
#             if start_date > end_date:
#                 raise forms.ValidationError(
#                     'The end date can\'t be before the start date.')

#     def save(self, user_id, commit=True):
#         order_item_id = self.cleaned_data['orderitem_id']
#         with agenda_def.keyword_agenda() as agenda:
#             description = {
#                 'keyword': str(self.cleaned_data['keyword']),
#                 'order_item_id': order_item_id,
#             }
#             orderitem_kw = CurrentEvent(
#                 agenda=agenda,
#                 title=_('keyword'),
#                 description=json.dumps(description),
#                 start_date=self.cleaned_data['start_date'],
#                 end_date=self.cleaned_data['end_date'],
#                 created_by=user_id,
#             )
#             orderitem_kw.save()
#         OrderItem.objects.get(pk=order_item_id).keyword_events.add(orderitem_kw)
#         return orderitem_kw


# class ChangePriceOnDate(forms.Form):
#     """Form to make a price change on a defined date.

#     It only created an event to change the name on the specified
#     date. The actual change in the db will be done by ???"""

#     orderitem_id = forms.ChoiceField(
#         choices=OrderItem.as_id_name_choices_tuple,
#         required=True,
#         )

#     start_date = forms.DateField(
#         label=_('start date'),
#         initial=tz.now().date(),
#         validators=[validators.MinValueValidator(
#             tz.now().date(),
#             _('Start date is already past, you can\'t deliver then anymore!')),
#         ],
#         required=True,
#     )

#     new_price = forms.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         required=True,
#     )

#     def save(self, user_id, commit=True):
#         order_item_id = self.cleaned_data['orderitem_id']
#         with agenda_def.pricing_agenda() as agenda:
#             description = {
#                 'newPrice': str(self.cleaned_data['new_price']),
#                 'order_item_id': order_item_id,
#             }
#             price_change = CurrentEvent(
#                 agenda=agenda,
#                 title=_('price change'),
#                 description=json.dumps(description),
#                 start_date=self.cleaned_data['start_date'],
#                 created_by=user_id,
#             )
#             price_change.save()
#         OrderItem.objects.get(pk=order_item_id).price_events.add(price_change)
#         return price_change


# class SpecialPriceOnKeyword(forms.Form):
#     """Form to show a price and for a keyword on a certain date.

#     It only create an event with the information as description the
#     implementation will be done in ???"""

#     orderitem_id = forms.ChoiceField(
#         label=_('Order item'),
#         choices=OrderItem.as_id_name_choices_tuple,
#         required=True,
#         )

#     start_date = forms.DateField(
#         label=_('start date'),
#         initial=tz.now().date(),
#         validators=[validators.MinValueValidator(
#             tz.now().date(),
#             _('Start date is already past, you can\'t deliver then anymore!')),
#         ],
#         required=True,
#     )

#     end_date = forms.DateField(
#         label=_('end date'),
#         required=True,
#     )

#     keyword = forms.CharField(
#         label=_('keyword'),
#         max_length=10,
#         required=True,
#     )

#     new_price = forms.DecimalField(
#         label=_('new price'),
#         max_digits=10,
#         decimal_places=2,
#         required=True,
#     )

#     def clean(self):
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get('start_date')
#         end_date = cleaned_data.get('end_date')

#         if start_date and end_date:
#             if start_date > end_date:
#                 raise forms.ValidationError(
#                     'The end date can\'t be before the start date.')

#     def save(self, user_id, commit=True):
#         order_item_id = self.cleaned_data['orderitem_id']
#         with agenda_def.pricing_agenda() as agenda:
#             description = {
#                 'newPrice': str(self.cleaned_data['new_price']),
#                 'order_item_id': order_item_id,
#                 'keyword': self.cleaned_data['keyword'],
#             }
#             kw_price = CurrentEvent(
#                 agenda=agenda,
#                 title=_('event_price'),
#                 description=json.dumps(description),
#                 start_date=self.cleaned_data['start_date'],
#                 end_date=self.cleaned_data['end_date'],
#                 created_by=user_id,
#             )
#             kw_price.save()
#         OrderItem.objects.get(pk=order_item_id).price_events.add(kw_price)
#         return kw_price


# class AssemblyPointPromotion(forms.Form):
#     """Form to create and manage promotions for assembly point deliveries."""

#     orderitem_id = forms.ChoiceField(
#         label=_('Order item'),
#         choices=OrderItem.as_id_name_choices_tuple,
#         required=True,
#         )

#     start_date = forms.DateField(
#         label=_('start date'),
#         validators=[validators.MinValueValidator(
#             tz.now().date(),
#             _('Date is already past, you can\'t deliver then anymore!')),
#         ],
#         required=True,
#     )

#     end_date = forms.DateField(
#         label=_('end date'),
#         required=True,
#     )

#     new_price = forms.DecimalField(
#         label=_('new price'),
#         max_digits=10,
#         decimal_places=2,
#         required=True,
#     )

#     def clean(self):
#         cleaned_data = super().clean()
#         order_item_id = cleaned_data.get('orderitem_id')
#         start_date = cleaned_data.get('start_date')
#         end_date = cleaned_data.get('end_date')
#         new_price = cleaned_data.get('new_price')

#         if start_date and end_date:
#             if start_date > end_date:
#                 raise forms.ValidationError(
#                     'The end date can\'t be before the start date.')
#             if order_item_id and new_price:
#                 self.kw_event = OrderItemKeyword({
#                     'orderitem_id': order_item_id,
#                     'start_date': start_date,
#                     'end_date': end_date,
#                     'keyword': agenda_def.EVENT_KW_ASSEMBLY_POINT_PROMOTION})
#                 if not self.kw_event.is_valid():
#                     raise forms.ValidationError(
#                         'Can not save this requests kw_event?')
#                 self.spok_event = SpecialPriceOnKeyword({
#                     'orderitem_id': order_item_id,
#                     'start_date': start_date,
#                     'end_date': end_date,
#                     'keyword': agenda_def.EVENT_KW_ASSEMBLY_POINT_PROMOTION,
#                     'new_price': new_price,
#                 })
#                 if not self.spok_event.is_valid():
#                     raise forms.ValidationError(
#                         'Can not save this requests spok event?')

#     def save(self, user_id, commit=True):
#         self.kw_event.save(user_id)
#         self.spok_event.save(user_id)

import logging
import re
import datetime

from django.conf import settings
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.forms import formset_factory
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.contrib.auth.decorators import permission_required

from . import forms, models
from .cart import ALL, OrderInfo, Cart
# from .models import OrderItem, DeliveryAddress, Order
from .forms import DeliveryAddressForm
import orders.agenda as agenda_def

import mb.menu as tab
from food.models import FOOD_CATEGORY
from address.forms import AddressForm
from agenda.models import CurrentEvent

logger = logging.getLogger(__name__)

#####
#
# product listing pages
#


class OrderItemList(ListView):
    queryset = models.OrderItem.objects.filter(
        product_foodproduct__category=FOOD_CATEGORY['lunch']
        ).filter(listview_show=True).order_by('listview_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['check_menu_item'] = 'lunch'
        return context


class DessertList(ListView):
    queryset = models.OrderItem.objects.filter(
        product_foodproduct__category=FOOD_CATEGORY['dessert']
        ).filter(listview_show=True).order_by('listview_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['check_menu_item'] = 'dessert'
        return context


#####
#
# address pages
#

class DeliveryAddressList(PermissionRequiredMixin, ListView):

    permission_required = 'is_staff'
    model = models.DeliveryAddress

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['check_menu_item'] = 'staff'
        return context


class DeliveryAddressDetail(PermissionRequiredMixin, DetailView):

    permission_required = 'is_staff'
    model = models.DeliveryAddress

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['check_menu_item'] = 'staff'
        context['scheduled_deliveries'] = (
            context['deliveryaddress'].deliveries.all())
        print('>>>>>', context['scheduled_deliveries'])
        return context


class add_delivery_address(PermissionRequiredMixin, View):

    permission_required = 'is_staff'

    http_method_names = ['get', 'post']
    title = _('Add delivery address')
    template_name = 'orders/set_delivery_address.html'
    form = forms.DeliveryAddressForm

    def get(self, request):
        form = DeliveryAddressForm()
        request_dict = {
            'form': form,
            'check_menu_item': 'staff',
        }
        return render(request, self.template_name, request_dict)

    def post(self, request):
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff_menu'))
        request_dict = {
            'form': form,
            'check_menu_item': 'staff',
        }
        return render(request, self.template_name, request_dict)


class AddDeliveryDateForDeliveryAddress(PermissionRequiredMixin, View):

    permission_required = 'is_staff'

    http_method_names = ['get', 'post']
    next_url = 'orders:deliveryaddress_detail'
    template_name = 'orders/add_delivery_date.html'
    form = forms.DeliveryDateForDeliveryAddressForm

    request_dict = {
        'check_menu_item': 'staff',
        'title': _('Add delivery date for delivery address.'),
        'submit_text': _('add'),
    }

    def get(self, request, pk):
        form = self.form()
        request_dict = {
            'form': form,
            'pk': pk,
            'address_name': models.DeliveryAddress.objects.get(pk=pk).address.address_name,
        }
        self.request_dict.update(request_dict)
        return render(request, self.template_name, self.request_dict)

    def post(self, request, pk):
        form = self.form(request.POST)
        if form.is_valid():
            form.save(models.DeliveryAddress.objects.get(pk=pk))
            return HttpResponseRedirect(reverse(self.next_url, args=pk))
        request_dict = {
            'form': form,
            'pk': pk,
            'address_name': models.DeliveryAddress.objects.get(pk=pk).address.address_name,
        }
        self.request_dict.update(request_dict)
        return render(request, self.template_name, self.request_dict)


#####
#
# cart managing pages
#

class add_to_cart_xhtml_response(View):

    http_method_names = ['post']
    form = forms.AddToCartForm

    def extra_form_parameters(self, request):
        return dict()

    @staticmethod
    def info(cleaned_data):
        return OrderInfo()

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            extra_form_parameters = self.extra_form_parameters(request)
            form = self.form(request.POST,
                             **extra_form_parameters)
            if form.is_valid():
                product = form.cleaned_data['product']
                cart = request.session['cart']
                cart.add_items(
                    product,
                    form.cleaned_data['number'],
                    self.info(form.cleaned_data)
                )
                return JsonResponse(
                    {'responseText': self.form(
                        initial={
                            'product': form.cleaned_data['product']},
                        **extra_form_parameters).as_p(),
                     'itemsInCart': cart.count(ALL),
                     'Cart_content': str(cart),
                     })
        logger.warning("add_to_cart_xml, bad request")
        return HttpResponse(form.as_p(), status=400)


class add_to_cart(add_to_cart_xhtml_response):

    form = forms.AddToCartForm


class add_to_cart_with_date_info(add_to_cart_xhtml_response):

    form = forms.AddToCartWithDateInfo

    @staticmethod
    def info(cleaned_data):
        item_info = OrderInfo()
        item_info['delivery_date'] = str(cleaned_data['delivery_date'])
        return item_info


class add_to_cart_with_extra_requests_info(add_to_cart_xhtml_response):

    form = forms.AddToCartWithExtraRequestsInfo

    @staticmethod
    def info(cleaned_data):
        item_info = OrderInfo()
        item_info['special_requests'] = str(cleaned_data['special_requests'])
        return item_info


class add_to_cart_with_event_info(add_to_cart_xhtml_response):

    form = forms.AddToCartWithEventInfo

    def extra_form_parameters(self, request):
        p_dict = {
            'choice_list': request.user.client.deliveries_choice_tuple()}
        return p_dict

    @staticmethod
    def info(cleaned_data):
        item_info = OrderInfo()
        item_info['delivery_event_id'] = str(cleaned_data['delivery_event_id'])
        return item_info


class add_to_cart_with_event_extra_requests_info(add_to_cart_xhtml_response):

    form = forms.AddToCartWithEventExtraRequestsInfo

    def extra_form_parameters(self, request):
        p_dict = {
            'choice_list': request.user.client.deliveries_choice_tuple()}
        return p_dict

    @staticmethod
    def info(cleaned_data):
        item_info = OrderInfo()
        item_info['delivery_event_id'] = str(cleaned_data['delivery_event_id'])
        item_info['special_requests'] = str(cleaned_data['special_requests'])
        return item_info


class edit_cart(View):

    http_method_names = ['get', 'post']
    title = 'Shopping Cart'
    info = str

    def get(self, request):
        cart = request.session['cart']
        for line in cart.lines(request.user):
            print('>>', line)
        print(cart.as_info_ordered_cart(
            'delivery_event_id', Cart.delivery_event_name_and_start_date))
        cart_form = request.session['cart'].as_info_ordered_form(
            'delivery_event_id',
            Cart.delivery_event_name_and_start_date
        )
        var_map = {'title': self.title,
                   'cart_formText': render_to_string(
                       'orders/cart_form.html',
                       {'cart_form': cart_form})}
        return render(request, 'orders/edit_cart.html', var_map)

    def post(self, request):
        cart = request.session['cart']

        print(cart.lines())
        o_cart = cart.as_info_ordered_cart(
            'delivery_event_id', Cart.delivery_event_name_and_start_date)
        item, new_value = [x for x in request.POST.items()][0]
        base = re.match('(.*)-([0-9]*)-number$', item)
        item_nr = int(base.group(2))
        print(f'this is item {item_nr} in sub {base.group(1)} changing to {new_value}')
        # product_id, info = self.find_cart_item(cart, item_nr)
        # print(f'{product_id}, {info}')
        product_id, info = self.find_o_cart_item(
            o_cart, base.group(1), item_nr)
        cart.set_item(product_id, int(new_value), info)
        cart_form = request.session['cart'].as_info_ordered_form(
            'delivery_event_id',
            Cart.delivery_event_name_and_start_date
        )
        return JsonResponse(
            {'responseText': render_to_string(
                       'orders/cart_form.html',
                       {'cart_form': cart_form}),
             'itemsInCart': cart.count(ALL),
             'Cart_content': str(cart),
             })

    def create_cart_form(self, cart):
        cart_lines = []
        for product_id in cart:
            name = models.OrderItem.objects.get(pk=product_id).product.name
            for info in cart[product_id]:
                cart_lines.append({'number': cart[product_id][info],
                                   'product_id': product_id,
                                   'product_description': name,
                                   'info_description': OrderInfo(info),
                                   })
        return forms.cart_table(initial=cart_lines)

    def find_cart_item(self, cart, item_nr):
        count = 0
        for product_id in cart:
            for info in cart[product_id]:
                if count == item_nr:
                    return product_id, info
                count += 1
        raise IndexError()

    def find_o_cart_item(self, o_cart, group, item_nr):
        for group_name, cart_lines in o_cart:
            if group_name == group:
                cart_line = cart_lines[item_nr]
                return cart_line['product_id'], cart_line['info_key']


#####
#
# pricing and promotion
#

class AddPriceChangeOnDate(PermissionRequiredMixin, View):

    permission_required = 'is_staff'

    http_method_names = ['get', 'post']
    next_url = 'staff_menu'
    template_name = 'orders/staff_form.html'
    form = forms.PriceChangeOnDateForm

    request_dict = {
        'check_menu_item': 'staff',
        'title': _('Add date for permanent price change.'),
        'submit_text': _('add'),
    }

    def get(self, request):
        form = self.form()
        request_dict = {
            'form': form,
        }
        self.request_dict.update(request_dict)
        return render(request, self.template_name, self.request_dict)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(self.next_url))
        request_dict = {
            'form': form,
        }
        self.request_dict.update(request_dict)
        return render(request, self.template_name, self.request_dict)


class AssemblyPointPromotion(PermissionRequiredMixin, View):

    permission_required = 'is_staff'

    htp_method_names = ['get', 'post']
    next_url = 'staff_menu'
    template_name = 'orders/staff_form.html'
    form = forms.AssembyPointPromotionForm

    request_dict = {
        'check_menu_item': 'staff',
        'title': _('Add a delivery point promotion.'),
        'submit_text': _('add'),
    }

    def get(self, request):
        form = self.form()
        request_dict = {
            'form': form,
        }
        self.request_dict.update(request_dict)
        return render(request, self.template_name, self.request_dict)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(self.next_url))
        request_dict = {
            'form': form,
        }
        self.request_dict.update(request_dict)
        return render(request, self.template_name, self.request_dict)


class AssemblyPointPromotionList(PermissionRequiredMixin, View):

    permission_required = 'is_staff'

    http_method_names = ['get']
    title = _('Assemblypoint promotion list')
    template_name = 'orders/list_assemblypoint_promotions.html'

    def get(self, request):
        request_dict = {
            'title': self.title,
        }
        return self.promo_list()

    @staticmethod
    def promo_list():
        with agenda_def.keyword_agenda() as agenda:
            temp_set = CurrentEvent.objects.filter(agenda=agenda)
        temp_set = filter(agenda_def.is_assembly_point_promotion, temp_set)
        return sorted(
            temp_set,
            key=lambda x: (x.safe_start_datetime, x.order_item_id))


#####
#
# order management
#

class Order(PermissionRequiredMixin, View):

    permission_required = 'client.user_is_client'

    http_method_names = ['get', 'post']
    template_name = 'orders/place_order.html'
    request_dict = {
        'title': _('Order'),
    }

    def get(self, request):
        client = request.user.client
        cart = request.session['cart']
        order = cart.as_order(
            user=client.user,
            category_function=self.categorize,
            cart_info_function=self.special_request_info,
            address_function=self.address,
            delivery_date_function=self.date,
        )
        request_dict = {
            'order': order,
            # 'cat_order': self.to_categorized(order),
        }
        self.request_dict.update(request_dict)
        return render(request, self.template_name, self.request_dict)

    # @staticmethod
    # def to_categorized(order):
    #     cat_order = defaultdict(list)
    #     for orderline in order.orderline_set.all():
    #         cat_order[orderline.category].append(orderline)
    #     return cat_order

    @staticmethod
    def categorize(cartline):
        if 'delivery_event_id' in cartline['info']:
            event_id = cartline['info']['delivery_event_id']
            event = models.DeliveryDateForDeliveryAddress.objects.get(id=event_id)
            delivery_str = _('Delivery')
            title = (f'{event.safe_start_date} | '
                     f'{delivery_str} '
                     f'{event.delivery_address.address.address_name}')
            return (title)

    @staticmethod
    def special_request_info(info):
        return info['special_requests']

    @staticmethod
    def address(info):
        if 'delivery_event_id' in info:
            event_id = info['delivery_event_id']
            address = models.DeliveryDateForDeliveryAddress.objects.get(
                id=event_id).delivery_address.address
            return address
        return None

    @staticmethod
    def date(info):
        if 'delivery_event_id' in info:
            event_id = info['delivery_event_id']
            date = models.DeliveryDateForDeliveryAddress.objects.get(
                id=event_id).safe_start_date
            print(f'date is {date}')
            return date


class PayOrder(PermissionRequiredMixin, View):

    permission_required = 'client.user_is_client'
    http_method_names = ['get']

    def get(self, request, pk):
        return self.get_mollie_faker(request, pk)

    def get_mollie_faker(self, request, pk):
        order = models.Order.objects.get(pk=pk)
        mollie_dict = {
            'amount': order.total,
            'description': f'Web order {order.id}',
            'webhookUrl': reverse('orders:mollie_verification', args=[pk]),
            'redirectUrl': reverse('orders:order_payed', args=[pk]),
            'metadata': {'order_nr': pk}
        }
        print('--TEST-PAYING--')
        print('mollie dictionary')
        print(mollie_dict)
        order.state = order.PAYMENT_PENDING
        order.save()
        return redirect(reverse('orders:fake_mollie_server', args=[pk]))


def mollie_webhook_verification(request, pk):
    status = request.POST['status']
    print(f'received molly payment change announcement for {pk}')
    print(f'faked status: {status}')
    order = models.Order.objects.get(pk=pk)
    # Check by mollie api if order is payed.
    # if payment.isPaid()
    # if payment.isOpen()
    # if payment.isPending()
    # else canceled
    if status == 'cancelled':
        order.delete()
    elif status == 'paid':
        order.payment_confirmed(service='mollie', payment_id='test_id')
    return HttpResponse(status=200)


def order_payed(request, pk):
    cart = request.session['cart']
    cart.clear()
    request_dict = {
        'order_id': pk,
    }
    return render(request, 'orders/order_payed.html', request_dict)


class ShowOrdersForDate(PermissionRequiredMixin, View):

    permission_required = 'is_staff'

    http_method_names = ['get', 'post']
    form = forms.ADate

    def get(self, request):
        form = self.form()
        request_dict = {
            'form': form,
        }
        return tab.render_in_staff_tab(
            request, 'orders/get_order_date.html', request_dict)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            date = form.cleaned_data['adate']
            return HttpResponseRedirect(
                reverse('orders:orders_for_date',
                        args=[date.year, date.month, date.day]))
        request_dict = {
            'form': form,
        }
        return tab.render_in_staff_tab(
            request, 'orders/get_order_date.html', request_dict)

def orders_on_date(request, year, month, day):
    date = datetime.date(int(year), int(month), int(day))
    orders_on_date = models.Order.orderlines_as_category_table(
        models.OrderLine.objects.orders_on_date(date))
    return tab.render_in_staff_tab(request, 'orders/orders_on_date.html',
                                   {'date': date,
                                    'orders': orders_on_date})


#Fake mollie server page.
def fms(request, pk):
        return render(request, 'orders/fake_mollie_server_page.html', {'pk': pk})

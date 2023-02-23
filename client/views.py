import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from roce.forms import NewUser
from roce.helpers import all_valid
from roce.decorator_tests import is_anonymous

from .forms import ClientForm, ClientTelephoneForm, DeliveryAddressForm

from mb.menu import render_without_tab, render_in_info_tab
from address.forms import AddressForm
import orders.models

logger = logging.getLogger(__name__)

@permission_required('client.user_is_client')
def personal_info(request):
    return render_in_info_tab(request, 'client/personal_info.html')


@user_passes_test(is_anonymous)  # set redirect fieldname!!
def new(request):
    if request.method == 'POST':
        userform = NewUser(request.POST, prefix='user')
        clientform = ClientForm(request.POST, prefix='client')
        if all_valid(userform, clientform):  # , addressform):
            clientform.save(userform)  # , addressform)
            return HttpResponseRedirect(reverse('client:new_succes'))
    else:
        userform = NewUser(prefix='user')
        clientform = ClientForm(prefix='client')
    request_dict = {
        'userform': userform,
        'clientform': clientform,
        # 'check_menu_item': None,
        # 'addressform': addressform,
    }

    return render_without_tab(request, 'client/new.html', request_dict)


@user_passes_test(is_anonymous)
def new_succes(request):
    return render_without_tab(request, 'client/new_succes.html')


class SetChangeClientTelephone(PermissionRequiredMixin, View):

    permission_required = 'client.user_is_client'

    http_method_names = ['get', 'post']
    template_name = 'client/set_telephone.html'

    def get(self, request):
        client = request.user.client
        telephone = client.telephone
        if client.telephone:
            form = ClientTelephoneForm(initial={'telephone': telephone})
        else:
            form = ClientTelephoneForm()
        request_dict = {
            'form': form}
        return render_in_info_tab(request, self.template_name, request_dict)

    def post(self, request):
        client = request.user.client
        user_name = client.full_name()
        user_id = request.user.id
        form = ClientTelephoneForm(request.POST)
        if form.is_valid():
            client.telephone = form.cleaned_data['telephone']
            client.save()
            logger.info(
                f"{user_name}({user_id}) changed telephone number")
            return HttpResponseRedirect(reverse('client:personal_info'))
        return render_in_info_tab(request, self.template_name,
                                  {'form': form})


@permission_required("client.user_is_client")
def set_change_client_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            request.user.client.address = form.save()
            request.user.client.save()
            return HttpResponseRedirect(reverse('client:personal_info'))
    else:
        form = AddressForm(initial={'address_name': 'Thuisadres',
                                    'name': request.user.client.full_name(),
                                    'country': 'België',
                                    })

    request_dict = {
        'form': form,
    }

    return render_in_info_tab(request, 'client/set_address.html', request_dict)


class SetChangeDeliveryAddresses(PermissionRequiredMixin, View):

    permission_required = 'client.user_is_client'

    http_method_names = ['get', 'post']
    template_name = 'client/set_delivery_addresses.html'

    def get(self, request):
        address_choices = self.delivery_address_choices(
                request.user.client)
        if not address_choices:
            return HttpResponseRedirect(
                reverse('client:no_delivery_address_available'))
        form = DeliveryAddressForm(
            delivery_address_choice_list=self.delivery_address_choices(
                request.user.client))
        request_dict = {
            'form': form,
        }
        return render_in_info_tab(request, self.template_name, request_dict)

    def post(self, request):
        client = request.user.client
        form = DeliveryAddressForm(
            request.POST,
            delivery_address_choice_list=self.delivery_address_choices(client))
        if form.is_valid():
            user_name = client.full_name()
            user_id = request.user.id
            d_address = orders.models.DeliveryAddress.objects.get(
                    id=int(form.cleaned_data['delivery_address_id']))
            client.delivery_address.add(d_address)
            logger.info(f'{user_name}({user_id}) added {d_address}')
            return HttpResponseRedirect(reverse('client:personal_info'))
        request_dict = {
            'form': form,
        }
        return render_in_info_tab(request, self.template_name, request_dict)

    @staticmethod
    #  .values_list('id', 'address__address_name')
    # doesn't work? I guess it has something to do with deferred
    # fields?
    def delivery_address_choices(client):
        address_list_diff = orders.models.DeliveryAddress.objects.filter(
            show_in_client_options_p=True).difference(
                client.delivery_address.all())
        choices = [(d_adr.id, d_adr.address.address_name) for
                   d_adr in address_list_diff]
        return choices


@permission_required("client.user_is_client")
def no_delivery_address_available(request):
    return render_in_info_tab(request, 'client/no_delivery_address_available.html')


class DeleteDeliveryAddress(PermissionRequiredMixin, View):

    permission_required = 'client.user_is_client'

    http_method_names = ['get', 'post']
    template_name = 'client/delete_delivery_address.html'

    def get(self, request, address_id):
        # involved_address = DeliveryAddress.objects.get(id=address_id)
        involved_address = request.user.client.delivery_address.filter(
            id=address_id)
        if involved_address:
            request_dict = {
                'involved_address': involved_address[0],
                'check_menu_item': 'info',
            }
            return render_in_info_tab(
                request, self.template_name, request_dict)

    def post(self, request, address_id):
        client = request.user.client
        user_name = client.full_name()
        user_id = request.user.id
        if address_id == request.POST['address_id']:
            delivery_address = client.delivery_address.filter(
                id=address_id)
            if delivery_address:
                delivery_address = delivery_address[0]
                client.delivery_address.remove(delivery_address)
                logger.info(
                    f"{user_name}({user_id}) removed {delivery_address}")
        else:
            logger.security(
                f'{user_name} tried to remove delivery address {address_id}')
        return HttpResponseRedirect(reverse('client:personal_info'))


@permission_required("client.user_is_client")
def payed_orders(request):
    orderlist = orders.models.Order.orderlines_as_category_table(
        request.user.client.payed_items())
    return render_in_info_tab(request, 'client/payed_orders.html',
                              {'orderlist': orderlist})

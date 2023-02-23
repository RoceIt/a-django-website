from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import TEST_ADDRESS_PERMISSIONS
from .forms import AddressForm

from roce.helpers import next_or_home


class set_address(LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = TEST_ADDRESS_PERMISSIONS

    http_method_names = ['get', 'post']

    def get(self, request):
        form = AddressForm
        request_dict = {
            'form': form,
            #'next_page': request.GET['next']
        }
        return render(request, 'address/set_address.html', request_dict)

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            id_ = form.save().id
            redirect_to = next_or_home(request) + f"?id={id_}"
            return HttpResponseRedirect(redirect_to)
        request_dict = {
            'form': form,
            #'next_page': request.next_page,
        }
        return render(request, 'address/set_address.html', request_dict)


def seems_ok(request):
    # You can use this as a redirect when something is ok.
    return render(request, 'address/seemsok.html')

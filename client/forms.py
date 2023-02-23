"""Django forms for the client application.

Classes
=======
ClientForm: Insert a new client.

"""
from django import forms

from django.forms.models import ModelForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from .models import Client

# content_type = ContentType.objects.get_for_model(Client)
# clientPermission = Permission.objects.get(
#     content_type=ContentType.objects.get_for_model(Client),
#     codename='user_is_client')


class ClientForm(forms.models.ModelForm):
    """Model to create and change client settings."""

    field_order = ['telephone']

    class Meta:
        model = Client
        # fields = ['title', 'telephone']
        fields = ['telephone']

    def save(self, userform):  # , addressform):
        clientPermission = Permission.objects.get(
            content_type=ContentType.objects.get_for_model(Client),
            codename='user_is_client')
        user = userform.save(commit=True)
        # address = addressform.save()
        client = Client(
            # title=self.cleaned_data['title'],
            user=user,
            telephone=self.cleaned_data['telephone'],
            )  # address=address)
        client.save()
        # client.delivery.add(address)
        client.user.user_permissions.add(clientPermission)
        return client


class ClientTelephoneForm(forms.models.ModelForm):

    field_order = ['telephone']

    class Meta:
        model = Client
        # fields = ['title', 'telephone']
        fields = ['telephone']


class DeliveryAddressForm(forms.Form):

    delivery_address_id = forms.ChoiceField(
        label=_('delivery address'),
        choices=(),
        )

    def __init__(self, *args, **kwargs):
        d_address_choice_list = kwargs.pop('delivery_address_choice_list',
                                           None)
        super().__init__(*args, **kwargs)
        if d_address_choice_list:
            self.fields['delivery_address_id'].choices = d_address_choice_list

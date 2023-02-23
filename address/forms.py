"""Django forms for the address application.

Classes
=======
AddressForm: The basic form for the address model.

"""
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Address


class AddressForm(ModelForm):
    """The basic form for the address model."""
    class Meta:
        model = Address
        fields = ['address_name',
                  'name', 'name2',
                  'street', 'number', 'bus',
                  'postal_code', 'city',
                  'province', 'country']
       # labels = {
       #     'name': _('name'),}

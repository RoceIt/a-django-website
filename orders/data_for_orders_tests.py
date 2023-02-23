"""functions to create test orders models."""

import address
from .models import DeliveryAddress

ADDRESS = 'address'
KIND = 'kind'
SHOW_IN_CLIENT_OPTIONS = 'show_in_client_options_p'


def full_deliveryaddress_n(n):
    return {
        ADDRESS: address.models.Address.objects.create(
            **address.data_for_address_tests.full_address_n(n)),
        KIND: DeliveryAddress.KIND_OF_DELIVERY_CHOICES[0][0],
        SHOW_IN_CLIENT_OPTIONS: bool(n % 2),
    }

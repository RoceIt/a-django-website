from django.test import TestCase, Client

from . import models
from .cart import Cart
from . import data_for_orders_tests


class TestOrdersTestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.delivery_address1 = models.DeliveryAddress.objects.create(
            **data_for_orders_tests.full_deliveryaddress_n(1)
        )

    def test_full_deliveryaddress_n_ok(self):
        self.assertEqual(self.delivery_address1.address.address_name,
                         'address_name_1')
        self.assertEqual(self.delivery_address1.kind, 'FR')
        self.assertEqual(self.delivery_address1.show_in_client_options_p,
                         bool(1 % 2))


class TestCartImplemented(TestCase):
    def setUp(self):
        # Checking on requests so i need a client.
        self.client = Client()

    def test_session_is_assigned_a_cart(self):
        """Check if the session is assigned a Cart instance."""
        response = self.client.get('')
        session = self.client.session
        #print ([session.keys()])
        #self.assertTrue(isinstance(response.contextrequest['session']['cart'], Cart))

#class Test


class TestDeliveryAddressModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.d_address1 = models.DeliveryAddress.objects.create(
            **data_for_orders_tests.full_deliveryaddress_n(1)
        )

    def test_unique_id_str_ok(self):
        """
        Shot myself in the foot once by changinh this and loosing
        objects when filtering using this id string.
        """
        self.assertEqual(self.d_address1.unique_id_str,
                         '[1]Delivery (Free): address_name_1')

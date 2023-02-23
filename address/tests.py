from django.test import TestCase

from .models import Address
from . import data_for_address_tests


class TestAddressTestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address1 = Address.objects.create(
            **data_for_address_tests.full_address_n(1)
            )

    def test_full_address_n_ok(self):
        self.assertEqual(self.address1.address_name, 'address_name_1')
        self.assertEqual(self.address1.name, 'name_1')
        self.assertEqual(self.address1.name2, 'name2_1')
        self.assertEqual(self.address1.street, 'street_1')
        self.assertEqual(self.address1.number, '1')
        self.assertEqual(self.address1.bus, '1')
        self.assertEqual(self.address1.postal_code, 'B1111')
        self.assertEqual(self.address1.city, 'city_1')
        self.assertEqual(self.address1.province, 'province_1')
        self.assertEqual(self.address1.country, 'country_1')

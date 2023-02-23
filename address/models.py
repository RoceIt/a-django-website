"""A django address interface.

An address application for django.

Classes
=======

Address:  A basic named address.

"""
from django.db import models
from django import forms
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class Address(models.Model):
    """A named address.

    Properties
    ==========

    address_name: The name you want to give to the address.
    name: The first line for the name.
    name2: The second line for the name.
    street: The name of the street.
    number: The number of the house.
    bus: The bus number at the address.
    postal_code: The city's postal code.
    city: The name of the city/town.
    province: The province the address is in.
    country: The country the address is in.
    """

    address_name = models.CharField(
        # Translators: The name of an address.
        _('location name'),
        max_length=50,
        help_text=_("You're name to refer to this address."),
    )
    name = models.CharField(
        _('name'),
        max_length=120)
    name2 = models.CharField(
        _('name (2Nd line)'),
        max_length=120,
        blank=True)
    street = models.CharField(
        _('street'),
        max_length=80)
    number = models.CharField(
        # Translators: The house number in an address.
        _('number'),
        max_length=10,
    )
    bus = models.CharField(
        # Translators: The bus number in an address.
        _('bus'),
        max_length=10,
        blank=True,
    )
    postal_code = models.CharField(
        _('postal code'),
        max_length=15)
    city = models.CharField(
        _('city'),
        max_length=80)
    province = models.CharField(
        _('province'),
        max_length=80,
        blank=True,
    )
    country = models.CharField(
        # Translators: A country, something with a government.
        _('country'),
        max_length=80)

    class Meta:
        verbose_name = _('address')           # for translating
        verbose_name_plural = _('addresses')  # for translating

    def __str__(self):
        show = (self.name, self.address_name,)
        return '{} ({})'.format(*show)

    def as_p(self):
        return render_to_string('address/short_as_p.html', {'address': self})

    @classmethod
    def as_id_name_choices_tuple(cls):
        return cls.objects.values_list('id', 'name').order_by('name')


TEST_ADDRESS_PERMISSIONS = (
    'address.delete_address', 'address.change_address', 'address.add_address',)

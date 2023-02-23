"""Functions to shorten some longer lines.

all_valid(list_of_forms): Check if forms are valid.
next_or_home: Give the url of the next page in the request.GET.

"""
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

import django.forms


def all_valid(*forms):
    """
    Check if all forms are valid.

    Functions returns a Boolean.
    """
    for form in forms:
        if form.is_valid():
            continue
        return False
    return True


def next_or_home(request, home='/'):
    """Checks if next is in the requests GET data and returns the reverse
    url.  If not home is returned.

    """
    redirect_to = request.GET.get('next', None)
    if redirect_to:
        redirect_to = reverse(redirect_to)
    else:
        redirect_to = '/'
    return redirect_to


#####
#
# Data- en formfield helpers
#

def as_choice_tuple(data_list, text_fun, id_fun=lambda x: x.id,):
    """Return a list as a choicetuple"""
    choices = []
    if data_list:
        for item in data_list:
            choices.append((id_fun(item), text_fun(item)))
    return tuple(choices)


def clean_date_gte(
        form, fieldname, min_value,
        mssg=_('%(fieldname)s must be %(min_value)s or later'),
        code='invalid',
        params=None
        ):
    """Check if field 'fieldname' is greater or equal to min_value."""
    data = form.cleaned_data[fieldname]
    if params is None:
        params = {'fieldname': fieldname, 'min_value': str(min_value)}
    if data is None or data < min_value:
        raise django.forms.ValidationError(mssg, code=code, params=params)
    return data


def clean_field_required(
        form, fieldname,
        mssg=_('%(fieldname)s can not be empty'),
        code='invalid',
        params=None
        ):
    data = form.cleaned_data[fieldname]
    if params is None:
        params = {'fieldname': fieldname}
    if data is None:
        raise django.forms.ValidationError(mssg, code=code, params=params)
    return data

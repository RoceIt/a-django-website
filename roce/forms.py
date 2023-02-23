"""Some forms I would expect to be in the default Django implementation.

Maybe they are somewhere out there django is so huge.

"""
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField

ROCE_DATETIME_FORMATS = [
    '%d/%m/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
    '%d/%m/%Y %H:%M',       # '10/25/2006 14:30'
    '%d/%m/%Y',             # '10/25/2006'
    '%d/%m/%y %H:%M:%S',    # '10/25/06 14:30:59'
    '%d/%m/%y %H:%M',       # '10/25/06 14:30'
    '%d/%m/%y',             # '10/25/06'
]


class NewUser(UserCreationForm):
    """Model create all User items.

    Did not a basic userform with all items? Maybe it's somewhere out
    there?

    """
    first_name = CharField(
        max_length=30,
        label=_('first name'),
    )
    last_name = CharField(
        max_length=30,
        label=_('last name'),
    )
    email = EmailField(
        label=_('email'),
    )

    # field_order = ['first_name', 'last_name', 'email'
    #                'username', 'password1', 'password2']

    def save(self, commit=True):
        new_user = super(NewUser, self).save(commit=False)
        new_user.email = self.cleaned_data['email']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.first_name = self.cleaned_data['first_name']
        if commit:
            new_user.save()
        return new_user

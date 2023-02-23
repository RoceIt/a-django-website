from django import forms
from django.utils import timezone

class DeliveryDateInfoForm(forms.Form):

    delivery_date = forms.DateField(
        label='delivery_date',
        initial=timezone.now(),
    )

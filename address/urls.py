"""address application URL configuration.

I think I'll use this only for testing the application setup since I
guess this app will only be used for the forms and the db functionality.

"""

from django.conf.urls import url

from . import views

app_name = 'address'

urlpatterns = [
    url(r'^address/$', views.set_address.as_view(), name='address_form'),
    url(r'^seems_ok/$', views.seems_ok, name='seems_ok'),
]

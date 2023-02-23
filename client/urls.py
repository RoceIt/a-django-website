from django.conf.urls import url

from . import views

app_name = 'client'

urlpatterns = [
    url(r'^$', views.personal_info, name='personal_info'),
    url(r'^new$', views.new, name='new_client'),
    url(r'^new_succes$', views.new_succes, name='new_succes'),
    url(r'^set_telephone$', views.SetChangeClientTelephone.as_view(),
        name='set_telephone'),
    url(r'^set_address$', views.set_change_client_address,
        name='set_address'),
    url(r'^set_delivery_addresses',
        views.SetChangeDeliveryAddresses.as_view(),
        name='set_delivery_addresses'),
    url(r'^no_delivery_address_available', views.no_delivery_address_available,
        name='no_delivery_address_available'),
    url(r'^delete_delivery_addres/(?P<address_id>[0-9]+)/$',
        views.DeleteDeliveryAddress.as_view(), name='delete_delivery_address'),
    url(r'^payed_orders', views.payed_orders, name='payed_orders'),
]

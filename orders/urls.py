from django.conf.urls import url

from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^items$', views.OrderItemList.as_view(), name='items'),
    url(r'^dessert$', views.DessertList.as_view(), name='desserts'),
    # Cart management
    url(r'^add_to_cart$', views.add_to_cart.as_view(), name='add_to_cart'),
    url(r'^add_to_cart_with_date_info$',
        views.add_to_cart_with_date_info.as_view(),
        name='add_to_cart_with_date_info'),
    url(r'^add_to_cart_with_event_info$',
        views.add_to_cart_with_event_info.as_view(),
        name='add_to_cart_with_event_info'),
    url(r'^add_to_cart_with_extra_requests_info$',
        views.add_to_cart_with_extra_requests_info.as_view(),
        name='add_to_cart_with_extra_requests_info'),
    url(r'^add_to_cart_with_event_extra_requests_info$',
        views.add_to_cart_with_event_extra_requests_info.as_view(),
        name='add_to_cart_with_event_extra_requests_info'),
    url(r'^edit_cart$', views.edit_cart.as_view(), name='edit_cart'),
    url(r'^order$', views.Order.as_view(), name='place_order'),
    # Delivery management
    url(r'^delivery_address/(?P<pk>[0-9]+)/$',
        views.DeliveryAddressDetail.as_view(),
        name='deliveryaddress_detail'),
    url(r'^delivery_addresses$',
        views.DeliveryAddressList.as_view(),
        name='deliveryaddress_list'),
    url(r'^add_delivery_address$',
        views.add_delivery_address.as_view(),
        name='add_delivery_address'),
    url(r'^add_delivery_date/(?P<pk>[0-9]+)/$',
        views.AddDeliveryDateForDeliveryAddress.as_view(),
        name='add_delivery_date'),
    url(r'^get_order_date/$',
        views.ShowOrdersForDate.as_view(),
        name='get_order_date'),
    url(r'^get_order_date/(?P<year>\d{4})/(?P<month>\d\d?)/(?P<day>\d\d?)/$',
        views.orders_on_date,
        name='orders_for_date'),
    # Price management
    url(r'^change_price_on_date',
        views.AddPriceChangeOnDate.as_view(),
        name='change_price_on_date'),
    url(r'^set_assembly_point_promotion',
        views.AssemblyPointPromotion.as_view(),
        name='assembly_point_promotion'),
    # Payment
    url(r'pay_order/(?P<pk>[0-9]+)/$',
        views.PayOrder.as_view(),
        name="pay_order"),
    url(r'^mollie-webhook-verification/(?P<pk>[0-9]+)/$',
        views.mollie_webhook_verification,
        name='mollie_verification'),
    url(r'^order_payed/(?P<pk>[0-9]+)/$',
        views.order_payed,
        name='order_payed'),
    url(r'^fake_mollie_server/(?P<pk>[0-9]+)/$',
        views.fms, name='fake_mollie_server'),

]

from django.contrib import admin

from .models import *

#class OrderItemInline(admin.StackedInline):
#    model = OrderItem

admin.site.register(OrderItem)
admin.site.register(DeliveryAddress)
admin.site.register(DeliveryDateForDeliveryAddress)
admin.site.register(PriceChangeOnDate)
admin.site.register(AssemblyPointPromotion)
admin.site.register(OrderLine)
admin.site.register(Order)
admin.site.register(Deposit)

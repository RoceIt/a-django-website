from django.contrib import admin

from orders.models import OrderItem
#from orders.admin import OrderItemInline
from .models import Ingredient, Recepy, IngredientLine, FoodProduct, Packing, Allergen

class IngredientlineInline(admin.TabularInline):
    model = IngredientLine
    extra = 3

# class OrderItemInline(admin.StackedInline):
#     model = OrderItem
#     fk
    _name = 'product_foodproduct'

@admin.register(Recepy)
class RecepyAdmin(admin.ModelAdmin):
    inlines = (IngredientlineInline,)

# @admin.register(FoodProduct)
# class FoodProductAdmin(admin.ModelAdmin):
#     inlines = (OrderItemInline,)

admin.site.register(Ingredient)
admin.site.register(Packing)
admin.site.register(FoodProduct)
admin.site.register(Allergen)

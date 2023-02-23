from django.contrib import admin

from .models import Ingredient, Recepy, IngredientLine, FoodProduct, Packing

class IngredientlineInline(admin.TabularInline):
    model = IngredientLine
    extra = 3


@admin.register(Recepy)
class RecepyAdmin(admin.ModelAdmin):
    inlines = (IngredientlineInline,)

admin.site.register(Ingredient)
admin.site.register(Packing)
admin.site.register(FoodProduct)

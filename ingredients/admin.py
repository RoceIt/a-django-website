from django.contrib import admin
from .models import BaseIngredients, Vitamins, Minerals, NutritionalValues, Allergens

admin.site.register(BaseIngredients)
admin.site.register(Vitamins)
admin.site.register(NutritionalValues)
admin.site.register(Allergens)
admin.site.register(Minerals)

# Register your models here.

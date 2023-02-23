from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import FoodProduct
from .forms import DeliveryDateInfoForm

class FoodProductList(ListView):
    model = FoodProduct


class FoodProductDetail(DetailView):
    model = FoodProduct

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_info'] = DeliveryDateInfoForm
        context['ingredients'] = ', '.join(
            [x.name for x in self.object.online_ingredient_list()])
        context['allergens'] = ', '.join(
            [x.name for x in self.object.allergen_set()])
        return context

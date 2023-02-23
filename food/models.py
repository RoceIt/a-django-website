from operator import attrgetter

from django.db import models
from django.utils.translation import ugettext_lazy as _

from orders.models import OrderItem
from .intermediate_models import Quantity

FOOD_CATEGORY = {
    'lunch': 1,
    'dessert': 2,
    }


class Allergen(models.Model):
    """Possible allergens.

    Properties
    ==========
    Name
    """
    name = models.CharField(
        'name',
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'name',
        max_length=50,
        help_text='unique name to identify this ingredient',
        unique=True,
    )
    the_recepy = models.OneToOneField(
        'Recepy',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    allergens = models.ManyToManyField(
        Allergen,
        blank=True,
    )

    def __str__(self):
        return self.name

    @property
    def ingredient_is_recepy(self):
        if self.the_recepy:
            return True
        return False

    def base_ingredients(self, checked):
        if self.name in checked:
            return (set(), checked)
        checked.add(self.name)
        if self.ingredient_is_recepy:
            return (self.the_recepy.base_ingredient_set(checked), checked)
        else:
            return ({self}, checked)


class Recepy(models.Model):
    name = models.CharField(
        'name',
        max_length=50,
        help_text='Unique name to identify this recepy',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientLine',
    )

    def __str__(self):
        return self.name

    def online_ingredient_list(self):
        return [x.ingredient for
                x in self.ingredientline_set.filter(show_online=True)]

    def base_ingredient_set(self, checked=None):
        ingredient_set = set()
        if checked is None:
            checked = set()
        for ingredient in self.ingredients.all():
            new_ingredients, checked = ingredient.base_ingredients(checked)
            ingredient_set.update(new_ingredients)
        return ingredient_set

    def allergens(self):
        allergens = set()
        for ingredient in self.base_ingredient_set():
            allergens.update(ingredient.allergens.all())
        return allergens


class IngredientLine(Quantity):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recepy = models.ForeignKey(Recepy, on_delete=models.PROTECT)
    show_online = models.BooleanField(
        'show online',
        default=True,
        help_text='Show in online ingredient lists',
    )
    show_on_label = models.BooleanField(
        'show on label',
        default=True,
        help_text='Show on printed labels',
    )


class Packing(models.Model):
    name = models.CharField(
        _('name'),
        max_length=50,
    )
    contents = models.SmallIntegerField(
        _('contents'),
        help_text='contents in milliliter')
    weight = models.SmallIntegerField(
        _('weight'),
        help_text='weight in grams',
    )
    deposit = models.BooleanField(
        _('deposit'),
    )

    deposit_value = models.DecimalField(
        _('deposit value'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        )

    def __str__(self):
        return '{name} ({contents}ml)'.format(
            name=self.name,
            contents=self.contents,
            )


class FoodProduct(models.Model):
    UNIT_CHOICES = (
        (Quantity.MILLILITER, 'milliliter'),
        (Quantity.GRAMS, 'grams'),
        (Quantity.PIECE, 'piece'),
    )

    FOOD_CATEGORY_CHOICES = (
        (FOOD_CATEGORY['lunch'], 'lunch'),
        (FOOD_CATEGORY['dessert'], 'dessert'),
    )
    name = models.CharField(
        'name',
        max_length=50,
        help_text='unique name to identify the product',
        unique=True,
    )

    website_name = models.CharField(
        'website name',
        max_length=50,
        help_text='name for site',
    )

    website_plural_name = models.CharField(
        'plural name',
        max_length=50,
        help_text='plural name on web pages',
        blank=True,
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
    )
    amount = models.SmallIntegerField(
        'amount',
        help_text='amount of ingredient in product',
    )
    unit = models.CharField(
        'unit',
        max_length=2,
        choices=UNIT_CHOICES)
    packing = models.ForeignKey(
        Packing,
        on_delete=models.PROTECT)
    category = models.SmallIntegerField(
        'category',
        choices=FOOD_CATEGORY_CHOICES,
        default='0',
    )
    web_photo = models.ImageField(
        upload_to='products/photos/',
    )

    website_detail_text = models.CharField(
        'website detail text',
        help_text='Promo text on detail page',
        max_length=200,
        blank=True)

    order = models.OneToOneField(
        OrderItem,
        on_delete=models.CASCADE,
        related_name='product_foodproduct',
        blank=True,
    )

    def __str__(self):
        return self.name

    @property
    def product_is_recepy(self):
        if self.ingredient.the_recepy:
            return True
        return False

    def online_ingredient_list(self):
        if self.product_is_recepy:
            return self.ingredient.the_recepy.online_ingredient_list()
        else:
            return []

    def allergen_set(self):
        if self.product_is_recepy:
            return self.ingredient.the_recepy.allergens()
        else:
            return set()

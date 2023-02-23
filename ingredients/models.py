"""A django ingredients interface

simple, What is this ingredient and what are its properties

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

class ValuesPer100g(models.Model):
    gram = models.DecimalField(
        # Translators: weight
        _('gram'),
        max_digits=6,
        decimal_places=3,
        help_text=_('per 100 g'),
    )
    def percentage_rdi(self):
        # If it is possible?
        pass

class Allergens(models.Model):
    """Possible allergens.

    Properties
    ==========
    Name
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
    )
    #info =models.Charfield()
    #group = models.KeyField()
    #pictogram = models.image()?

    def __str__(self):
        return self.name

class NutritionalValues(models.Model):
    """Nutritional value values.

    Properties
    ==========
    Name
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
    )
    # Recommended daily intake
    rdi = models.DecimalField(
        # Translators: rdi, recommended daily intake
        _('RDI'),
        max_digits=6,
        decimal_places=3,
        help_text=_('recommended daily intake')
    )

    def __str__(self):
        return self.name

class NutritionalValueValues(ValuesPer100g):
    nutrition_value = models.ForeignKey(NutritionalValues, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('BaseIngredients', on_delete=models.CASCADE)



class Vitamins(models.Model):
    """Vitamins value values.

    Properties
    ==========
    name
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
    )
    # Recommended daily intake
    rdi = models.DecimalField(
        # Translators: rdi, recommended daily intake
        _('RDI'),
        max_digits=6,
        decimal_places=3,
        help_text=_('recommended daily intake')
    )

    def __str__(self):
        return self.name

class VitaminValues(ValuesPer100g):
    vitamin= models.ForeignKey(Vitamins, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('BaseIngredients', on_delete=models.CASCADE)



class Minerals(models.Model):
    """Vitamins value values.

    Properties
    ==========
    name
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
    )
    # Recommended daily intake
    rdi = models.DecimalField(
        # Translators: rdi, recommended daily intake
        _('RDI'),
        max_digits=6,
        decimal_places=3,
        help_text=_('recommended daily intake')
    )

    def __str__(self):
        return self.name


class MineralValues(ValuesPer100g):
    mineral = models.ForeignKey(Minerals, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('BaseIngredients', on_delete=models.CASCADE)


class BaseIngredients(models.Model):
    """A base ingredient.

    This is for base ingredients, that are not build of other
    ingredients.

    e.g. milk is a base ingredient, cheese is not
    Properties
    ==========

    name: the unique name for this particular ingredient.
    ingredient_list_name: official name.
    commercial_name: name you can use on the website, folder, ...
    unit: piece or weight (g)?
    allergen: known to be allergic list of allergen.
    picture: a picture of the product.
    """
    # Not for here, reuse it in a product model or something like that.
    # PIECE = 'P'
    # WEIGHT = 'W'
    # VOLUME = 'V'
    # UNIT_CHOICES = (
    #     (PIECE, _('piece')),
    #     (WEIGHT, _('weight')),
    #     (VOLUME, _('volume')),
    # )

    name = models.CharField(
        _('name'),
        max_length=50,
        help_text=_('A unique name for this product'),
        unique=True,
    )
    ingredient_list_name = models.CharField(
        _('ingredient list name'),
        max_length=30,
        help_text=_('Short name for ingredient lists,...'),
        blank=True,
    )
    commercial_name = models.CharField(
        _('commercial name'),
        max_length=50,
        help_text=_('Name to show on commercial info (site, folders, ...)'),
        blank=True
    )
    # unit = models.CharField(
    #     _('unit'),
    #     max_length=1,
    #     help_text=('The unit the ingredient is measured in.'),
    # )
    allergens = models.ManyToManyField(
        Allergens,
        related_name=_('base_ingredients')
    )
    nutricionals = models.ManyToManyField(
        NutritionalValues,
        through='NutritionalValueValues',
        related_name=_('base_ingredients'),
    )
    vitamins = models.ManyToManyField(
        Vitamins,
        through='VitaminValues',
        related_name=_('base_ingredients'),
    )
    minerals = models.ManyToManyField(
        Minerals,
        through='MineralValues',
        related_name=_('base_ingredients'),
    )


    def __str__(self):
        return self.name

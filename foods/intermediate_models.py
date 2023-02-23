from django.db import models

class Quantity(models.Model):
    PIECE = 'P'
    GRAMS = 'g'
    MILLIGRAMS = 'mg'
    LITER = 'l'
    CENTILITER = 'cl'
    MILLILITER = 'ml'
    QUANTITY_CHOICES = (
        (PIECE, 'piece'),
        (GRAMS, 'grams'),
        (MILLIGRAMS, 'milligrams'),
        (LITER, 'liter'),
        (CENTILITER, 'centiliter'),
        (MILLILITER, 'milliliter'),
    )
    value = models.SmallIntegerField(
        'value',
        blank=True,
    )
    unit = models.CharField(
        'unit',
        max_length=2,
        choices=QUANTITY_CHOICES,
        blank=True,
    )

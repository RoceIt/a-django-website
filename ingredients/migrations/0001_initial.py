# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 15:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='BaseIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A unique name for this product', max_length=50, unique=True, verbose_name='name')),
                ('ingredient_list_name', models.CharField(blank=True, help_text='Short name for ingredient lists,...', max_length=30, verbose_name='ingredient list name')),
                ('commercial_name', models.CharField(blank=True, help_text='Name to show on commercial info (site, folders, ...)', max_length=50, verbose_name='commercial name')),
                ('allergens', models.ManyToManyField(related_name='base_ingredients', to='ingredients.Allergens')),
            ],
        ),
        migrations.CreateModel(
            name='Minerals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('rdi', models.DecimalField(decimal_places=3, help_text='recommended daily intake', max_digits=6, verbose_name='RDI')),
            ],
        ),
        migrations.CreateModel(
            name='NutritionalValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('rdi', models.DecimalField(decimal_places=3, help_text='recommended daily intake', max_digits=6, verbose_name='RDI')),
            ],
        ),
        migrations.CreateModel(
            name='ValuesPer100g',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gram', models.DecimalField(decimal_places=3, help_text='per 100 g', max_digits=6, verbose_name='gram')),
            ],
        ),
        migrations.CreateModel(
            name='Vitamins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('rdi', models.DecimalField(decimal_places=3, help_text='recommended daily intake', max_digits=6, verbose_name='RDI')),
            ],
        ),
        migrations.CreateModel(
            name='MineralValues',
            fields=[
                ('valuesper100g_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ingredients.ValuesPer100g')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.BaseIngredients')),
                ('mineral', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.Minerals')),
            ],
            bases=('ingredients.valuesper100g',),
        ),
        migrations.CreateModel(
            name='NutritionalValueValues',
            fields=[
                ('valuesper100g_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ingredients.ValuesPer100g')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.BaseIngredients')),
                ('nutrition_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.NutritionalValues')),
            ],
            bases=('ingredients.valuesper100g',),
        ),
        migrations.CreateModel(
            name='VitaminValues',
            fields=[
                ('valuesper100g_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ingredients.ValuesPer100g')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.BaseIngredients')),
                ('vitamin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.Vitamins')),
            ],
            bases=('ingredients.valuesper100g',),
        ),
        migrations.AddField(
            model_name='baseingredients',
            name='minerals',
            field=models.ManyToManyField(related_name='base_ingredients', through='ingredients.MineralValues', to='ingredients.Minerals'),
        ),
        migrations.AddField(
            model_name='baseingredients',
            name='nutricionals',
            field=models.ManyToManyField(related_name='base_ingredients', through='ingredients.NutritionalValueValues', to='ingredients.NutritionalValues'),
        ),
        migrations.AddField(
            model_name='baseingredients',
            name='vitamins',
            field=models.ManyToManyField(related_name='base_ingredients', through='ingredients.VitaminValues', to='ingredients.Vitamins'),
        ),
    ]

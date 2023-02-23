# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 14:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('food', '0003_foodproduct_web_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodproduct',
            name='order',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='product_foodproduct', to='orders.OrderItem'),
            preserve_default=False,
        ),
    ]

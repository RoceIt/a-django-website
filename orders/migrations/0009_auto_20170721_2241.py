# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 20:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20170621_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryaddress',
            name='address',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='address.Address'),
        ),
    ]

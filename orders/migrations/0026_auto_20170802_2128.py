# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-02 19:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0025_auto_20170802_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_orderlines', related_query_name='orders_orderline', to='address.Address'),
        ),
    ]

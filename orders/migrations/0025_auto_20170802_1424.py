# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-02 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_order_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_service',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]

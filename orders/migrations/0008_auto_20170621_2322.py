# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20170614_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryaddress',
            name='show_in_client_options_p',
            field=models.BooleanField(default=False, verbose_name="show in client's delivery address options"),
        ),
        migrations.AlterField(
            model_name='deliveryaddress',
            name='kind',
            field=models.CharField(choices=[('FR', 'Free'), ('NO', 'None'), ('AP', 'Assambly point')], default='NO', max_length=2, verbose_name='type'),
        ),
    ]
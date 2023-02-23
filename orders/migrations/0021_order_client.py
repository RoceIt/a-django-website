# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_auto_20170719_1330'),
        ('orders', '0020_auto_20170731_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.Client'),
        ),
    ]

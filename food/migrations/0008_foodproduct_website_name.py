# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_auto_20170424_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodproduct',
            name='website_name',
            field=models.CharField(default='oeps', help_text='name for site', max_length=50, verbose_name='website name'),
            preserve_default=False,
        ),
    ]

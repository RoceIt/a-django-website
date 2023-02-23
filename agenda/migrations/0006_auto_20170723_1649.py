# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 14:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_auto_20170722_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='archive_after',
            field=models.DurationField(choices=[(datetime.timedelta(0), 'now archive policy'), (datetime.timedelta(1), '1 day'), (datetime.timedelta(7), '7 days'), (datetime.timedelta(31), '1 month')], verbose_name='archive after'),
        ),
    ]

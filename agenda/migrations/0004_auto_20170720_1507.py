# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0003_auto_20170621_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivedevent',
            name='finished',
            field=models.BooleanField(default=False, verbose_name='finished'),
        ),
        migrations.AddField(
            model_name='currentevent',
            name='finished',
            field=models.BooleanField(default=False, verbose_name='finished'),
        ),
    ]

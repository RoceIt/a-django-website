# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20170308_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodproduct',
            name='web_photo',
            field=models.ImageField(default=0, upload_to='products/photos/'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 12:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0008_auto_20170726_1203'),
        ('address', '0002_auto_20170609_1526'),
        ('orders', '0017_auto_20170727_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssemblyPointPromotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='short description')),
                ('description', models.TextField(verbose_name='description')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='start time')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='end time')),
                ('location', models.CharField(blank=True, max_length=80, verbose_name='location')),
                ('created_by', models.CharField(blank=True, max_length=80, verbose_name='created by')),
                ('finished', models.BooleanField(default=False, verbose_name='finished')),
                ('promotion_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_assemblypointpromotions', related_query_name='orders_assemblypointpromotion', to='address.Address')),
                ('agenda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_assemblypointpromotions', related_query_name='orders_assemblypointpromotion', to='agenda.Agenda')),
                ('assemblypoint', models.ManyToManyField(to='orders.DeliveryAddress')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderItem', verbose_name='Promotion product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

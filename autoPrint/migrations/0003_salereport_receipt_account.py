# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-29 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoPrint', '0002_auto_20170627_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='salereport',
            name='receipt_account',
            field=models.IntegerField(default=None, verbose_name='附寄单证张数'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-29 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoPrint', '0004_auto_20170629_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salereport',
            name='receipt_account',
            field=models.IntegerField(null=True, verbose_name='附寄单证张数'),
        ),
    ]
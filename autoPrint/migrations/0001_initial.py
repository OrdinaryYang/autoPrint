# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-10 03:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PayCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, verbose_name='公司名称')),
                ('company_account', models.CharField(max_length=50, verbose_name='付款人账号')),
                ('company_address', models.CharField(max_length=200, verbose_name='付款人地址')),
                ('account_location', models.CharField(max_length=100, verbose_name='付款人开户行')),
                ('pay_province', models.CharField(max_length=100, verbose_name='省')),
                ('pay_city', models.CharField(max_length=100, verbose_name='市')),
            ],
        ),
        migrations.CreateModel(
            name='PayeeCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, verbose_name='公司名称')),
                ('company_account', models.CharField(max_length=50, verbose_name='收款人账号')),
                ('company_address', models.CharField(max_length=200, verbose_name='收款人地址')),
                ('account_location', models.CharField(max_length=100, verbose_name='收款人开户行')),
                ('notes', models.CharField(max_length=200, verbose_name='备注')),
                ('added_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加日期')),
                ('payee_province', models.CharField(max_length=100, verbose_name='省')),
                ('payee_city', models.CharField(max_length=100, verbose_name='市')),
            ],
        ),
        migrations.CreateModel(
            name='SaleReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_comp', models.CharField(max_length=100, verbose_name='调入单位')),
                ('tax_receipt', models.CharField(max_length=50, verbose_name='发票号')),
                ('receipt_amount', models.IntegerField(default=None, verbose_name='附寄单证张数')),
                ('total_price', models.FloatField(max_length=50, verbose_name='价税合计')),
                ('total_price_ch', models.CharField(blank=True, max_length=100, null=True, verbose_name='大写金额')),
                ('date', models.CharField(max_length=20, verbose_name='日报日期')),
                ('added_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加日期')),
            ],
        ),
    ]

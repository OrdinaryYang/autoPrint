# Create your models here.
from django.db import models
from datetime import datetime


class SaleReport(models.Model):
    payment_comp = models.CharField(max_length=100, verbose_name='调入单位')
    tax_receipt = models.CharField(max_length=50, verbose_name='发票号')
    receipt_amount = models.IntegerField(default=None, verbose_name='附寄单证张数')
    total_price = models.FloatField(max_length=50, verbose_name='价税合计')
    total_price_ch = models.CharField(max_length=100, verbose_name='大写金额', null=True, blank=True)
    date = models.CharField(max_length=20, verbose_name='日报日期')
    added_date = models.DateTimeField(default=datetime.now, verbose_name='添加日期')

    def __str__(self):
        return "销售日报数据——" + self.payment_comp


class PayCompany(models.Model):
    company_name = models.CharField(max_length=100, verbose_name='公司名称')
    company_account = models.CharField(max_length=50, verbose_name='付款人账号')
    company_address = models.CharField(max_length=200, verbose_name='付款人地址')
    account_location = models.CharField(max_length=100, verbose_name='付款人开户行')

    def __str__(self):
        return "付款人信息——" + self.company_name


class PayeeCompany(models.Model):
    company_name = models.CharField(max_length=100, verbose_name='公司名称')
    company_account = models.CharField(max_length=50, verbose_name='收款人账号')
    company_address = models.CharField(max_length=200, verbose_name='收款人地址')
    account_location = models.CharField(max_length=100, verbose_name='收款人开户行')
    notes = models.CharField(max_length=200, verbose_name='备注')
    added_date = models.DateTimeField(default=datetime.now, verbose_name='添加日期')

    def __str__(self):
        return "收款人信息——" + self.company_name

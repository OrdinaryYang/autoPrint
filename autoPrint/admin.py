from django.contrib import admin
from autoPrint.models import SaleReport, PayCompany, PayeeCompany

# Register your models here.
admin.site.register(SaleReport)
admin.site.register(PayeeCompany)
admin.site.register(PayCompany)
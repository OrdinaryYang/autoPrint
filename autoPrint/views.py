from django.core.files.storage import FileSystemStorage
from .models import PayCompany, PayeeCompany, SaleReport
from .config.myconfig import file_config
from django.shortcuts import render
from .lib.utils import accessExcelData, mergeDictsValue
from django.http import HttpResponse, JsonResponse
import logging
import os
import json
logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'autoPrint/upload.html')


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def check_info(request):
    json_info = json.dumps({'a': 1, 'b': 2})
    response = JsonResponse(json_info)
    return response


def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(base_url=file_config['base_url'], location=file_config['location'])
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename).lstrip('/')
        raw_info = accessExcelData(uploaded_file_url)
        comp_info = mergeDictsValue(raw_info)
        try:
            for k, v in comp_info.items():
                pay_company = PayCompany(company_name=k)
                sale_report = SaleReport(payment_comp=k, date=','.join(v[0]), total_price=v[1], total_price_cn=v[2],
                                         tax_receipt=','.join(v[3]))
                pay_company.save()
                sale_report.save()
                logger.debug('{comp_name}信息：{list}'.format(comp_name=k, list=str(v)))
            logger.info('日报信息提取完毕！')
            return render(request, 'autoPrint/index.html', {'file_url': uploaded_file_url})
        finally:
            os.remove(uploaded_file_url)
    else:
        return render(request, 'autoPrint/upload.html')

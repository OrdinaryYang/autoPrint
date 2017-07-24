import logging
import os
from .lib.utils_lan import email_verify
from django.core.files.storage import FileSystemStorage
from django.forms.models import model_to_dict
from .models import PayCompany, PayeeCompany, SaleReport
from .config.myconfig import file_config, acc_file_config, zip_file_config, ems_file_config
from django.shortcuts import render
from .lib.utils import accessExcelData, mergeDictsValue, write2csv, getToday, myCompress
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from collections import OrderedDict
from datetime import datetime


logger = logging.getLogger(__name__)
info = OrderedDict()


def home(request):
    return render(request, 'common/index.html')


def helper(request):
    return render(request, 'common/helper.html')


def test_details(request):
    return render(request, 'common/details.html')


def index(request):
    return render(request, 'common/index.html')


def logout(request):
    try:
        del request.session['USERNAME']
        del request.session['PASSWORD']
        del request.session['IS_LOGIN']
    except KeyError:
        pass
    return render(request, 'common/login.html')


def login(request):
    if 'IS_LOGIN' in request.session and request.session['IS_LOGIN']:
        username = request.session['USERNAME']
        name, server = username.split('@')
        return render(request, 'common/index.html', {'username': name})
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if email_verify(username, password) is True:
                request.session['IS_LOGIN'] = True
                request.session['USERNAME'] = username
                request.session['PASSWORD'] = password
                name, server = username.split('@')
                return render(request, 'common/index.html', {'username': name})
        else:
            return render(request, 'common/login.html')


def check_info(request):
    comp_name = request.POST['name']
    pay_list = PayCompany.objects.filter(company_name=comp_name)
    sales_list = SaleReport.objects.filter(payment_comp=comp_name).order_by('added_date')
    payee_list = PayeeCompany.objects.all().order_by('added_date')
    if len(payee_list) == 0:
        payee = PayeeCompany()
    else:
        payee = payee_list[::-1][0]
    if len(pay_list) == 0:
        pay = PayeeCompany(company_name=comp_name)
    else:
        pay = pay_list[::-1][0]
    if len(sales_list) == 0:
        sales = SaleReport()
    else:
        sales = sales_list[::-1][0]
    dict_pay = model_to_dict(pay)
    dict_payee = model_to_dict(payee)
    dict_sales = model_to_dict(sales)
    data = {'pay': dict_pay, 'payee': dict_payee, 'sales': dict_sales}
    print(data)
    return JsonResponse(data)


def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(base_url=file_config['base_url'], location=file_config['location'])
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename).lstrip('/')
        raw_info = accessExcelData(uploaded_file_url)
        sales_info = mergeDictsValue(raw_info)
        global info
        info = sales_info
        try:
            for k, v in sales_info.items():
                sale_report = SaleReport(payment_comp=k, date=','.join(v[0]), total_price=v[1], total_price_ch=v[2],
                                         tax_receipt=','.join(v[3]), receipt_amount=len(v[3]))
                sale_report.save()
                logger.debug('{comp_name}信息：{list}'.format(comp_name=k, list=str(v)))
            logger.info('日报信息提取完毕！')
            return render(request, 'common/details.html', {'sales_info': sales_info, 'amount': len(sales_info)})
        finally:
            os.remove(uploaded_file_url)

            # 为两个输出csv文件设置标题栏
            file_name = file_config['csv_dir']
            acc_file_name = acc_file_config['acc_file_dir']
            ems_file_name = ems_file_config['ems_file_dir']
            dir_path = zip_file_config['dir_path']
            for file in os.listdir(dir_path):
                os.remove(dir_path+file)
            line = file_config['line']
            acc_line = acc_file_config['account_line']
            ems_line = ems_file_config['ems_line']
            write2csv(acc_file_name, [acc_line], mode='w')
            write2csv(file_name, [line], mode='w')
            write2csv(ems_file_name, [ems_line], mode='w')
    else:
        return render(request, 'common/upload.html')


def download(req):
    the_file_name = zip_file_config['file_name']
    csv_path = zip_file_config['dir_path']
    myCompress(csv_path, the_file_name)

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
            f.close()
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


def download_printer(req):
    the_file_name = zip_file_config['printer_path']

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
            f.close()
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


def post_details(request):
    if request.method == 'POST':
        # 付款人信息
        payment_comp = request.POST['pay_name']
        pay_company_account = request.POST['pay_account']
        pay_company_address = request.POST['pay_address']
        pay_account_location = request.POST['pay_location']
        pay_province = request.POST['pay_province']
        pay_city = request.POST['pay_city']
        pay = PayCompany.objects.filter(company_name=payment_comp)
        if len(pay) == 0:
            p1 = PayCompany(company_account=pay_company_account, company_address=pay_company_address,
                            account_location=pay_account_location, company_name=payment_comp, pay_city=pay_city,
                            pay_province=pay_province)
            p1.save()
        else:
            if payment_comp == pay[0].company_name \
                    and pay_company_account == pay[0].company_account \
                    and pay_company_address == pay[0].company_address \
                    and pay_account_location == pay[0].account_location:
                pass
            else:
                pay.update(company_account=pay_company_account, company_address=pay_company_address,
                           account_location=pay_account_location, company_name=payment_comp, pay_city=pay_city,
                           pay_province=pay_province)

        # 收款人信息
        payee_comp = request.POST['payee_name']
        payee_company_account = request.POST['payee_account']
        payee_company_address = request.POST['payee_address']
        payee_account_location = request.POST['payee_location']
        payee_province = request.POST['payee_province']
        payee_city = request.POST['payee_city']
        notes = request.POST['notes']
        payee = PayeeCompany.objects.filter(company_name=payee_comp)
        if len(payee) != 0:
            payee.update(company_account=payee_company_account, company_address=payee_company_address,
                         account_location=payee_account_location, notes=notes, payee_city=payee_city,
                         payee_province=payee_province, added_date=datetime.now())
        else:

            payee1 = PayeeCompany(company_name=payee_comp, company_account=payee_company_account,
                                  company_address=payee_company_address, account_location=payee_account_location,
                                  notes=notes, payee_city=payee_city, payee_province=payee_province)
            payee1.save()

        # 日报信息
        # sales_price_ch = request.POST['price_ch']
        sales_price = request.POST['price']
        sales_tax_receipt = request.POST['tax_receipt']
        sales_receipt_amount = request.POST['receipt_amount']
        sales_date = request.POST['date']
        year, month, day = sales_date.split('-')

        info_line = [[year, '\t'+month, '\t'+day, payment_comp, '\t'+pay_company_account, payee_comp,
                      '\t'+payee_company_account,
                      '款项用途', payee_account_location, sales_price, sales_price, '\t'+sales_tax_receipt, notes,
                      '款项接收日期', pay_account_location, pay_province, pay_city, payee_province, payee_city,
                      sales_receipt_amount], ]
        acc_info_line = [[getToday(), payment_comp, pay_province+pay_city+pay_account_location, sales_price,
                          't'+sales_tax_receipt, sales_receipt_amount, notes], ]
        ems_info_line = [[ems_file_config['company_from'], ems_file_config['company_from_addr'], payment_comp,
                         pay_company_address], ]
        write2csv(file_config['csv_dir'], info_line, mode='a')
        write2csv(acc_file_config['acc_file_dir'], acc_info_line, mode='a')
        write2csv(ems_file_config['ems_file_dir'], ems_info_line, mode='a')

        data = {'name': payment_comp}
        return JsonResponse(data)
        # return render(request, 'autoPrint/index.html', {'sales_info': sales_info, 'amount': len(sales_info)})


# 暂时没有用到
def get_details(request, comp_name, order):
    pay_list = PayCompany.objects.filter(company_name=comp_name)
    sales_list = SaleReport.objects.filter(payment_comp=comp_name).order_by('added_date')
    payee_list = PayeeCompany.objects.all().order_by('added_date')
    if len(payee_list) == 0:
        payee = PayeeCompany()
    else:
        payee = payee_list[::-1][0]
    if len(pay_list) == 0:
        pay = PayeeCompany(company_name=comp_name)
    else:
        pay = pay_list[::-1][0]
    if len(sales_list) == 0:
        sales = SaleReport()
    else:
        sales = sales_list[::-1][0]
    return render(request, 'autoPrint/details.html', {'pay': pay, 'order': order,
                                                      'payee': payee, 'sales': sales})



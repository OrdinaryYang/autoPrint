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
    """
    这事一个测试用的view，没有实际意义
    :param request:
    :return:
    """
    json_info = {'广东烟草佛山市有限责任公司': [['2017-03-09'], 885456.0, '捌拾捌万伍千肆百伍拾陆元整', ['00220670']], '中国烟草总公司北京市公司': [['2017-03-09'], 11177427.11, '壹千壹百壹拾柒万柒千肆百贰拾柒元壹角整', ['00220705', '00220706']], '湖北省烟草公司孝感市公司': [['2017-03-09'], 331203.6, '叁拾叁万壹千贰百零叁元陆角整', ['00220640']], '广西壮族自治区烟草公司梧州市公司': [['2017-03-09'], 221375.11, '贰拾贰万壹千叁百柒拾伍元壹角壹分', ['00220698']], '广西壮族自治区烟草公司柳州市公司': [['2017-03-09'], 442750.23, '肆拾肆万贰千柒百伍拾元贰角叁分', ['00220697']], '山东青岛烟草有限公司': [['2017-03-09'], 2708392.93, '贰百柒拾万捌千叁百玖拾贰元玖角贰分', ['00220660', '00220661', '00220662']], '辽宁省烟草公司沈阳市公司': [['2017-03-09'], 442750.23, '肆拾肆万贰千柒百伍拾元贰角叁分', ['00220688']], '黑龙江省烟草公司鸡西市公司': [['2017-03-09'], 220802.4, '贰拾贰万零捌百零贰元肆角整', ['00220643']], '湖南省烟草公司张家界市公司': [['2017-03-09'], 110687.56, '壹拾壹万零陆百捌拾柒元伍角伍分', ['00220704']], '广东烟草茂名市有限责任公司': [['2017-03-09'], 962205.43, '玖拾陆万贰千贰百零伍元肆角贰分', ['00220671']], '广东烟草河源市有限责任公司': [['2017-03-09'], 442728.0, '肆拾肆万贰千柒百贰拾捌元整', ['00220687']], '安徽省烟草公司铜陵市公司': [['2017-03-09'], 254100.02, '贰拾伍万肆千壹百元零壹分', ['00220692']], '山西省烟草公司朔州市公司': [['2017-03-09'], 2972422.91, '贰百玖拾柒万贰千肆百贰拾贰元玖角整', ['00220722']], '辽宁省烟草公司盘锦市公司': [['2017-03-09'], 481276.28, '肆拾捌万壹千贰百柒拾陆元贰角捌分', ['00220637']], '湖南省烟草公司怀化市公司': [['2017-03-09'], 846933.75, '捌拾肆万陆千玖百叁拾叁元柒角伍分', ['00220693']], '黑龙江省烟草公司哈尔滨市公司': [['2017-03-09'], 140794.99, '壹拾肆万零柒百玖拾肆元玖角玖分', ['00220655', '00220691']], '山西省烟草公司吕梁市公司': [['2017-03-09'], 3898325.57, '叁百捌拾玖万捌千叁百贰拾伍元伍角柒分', ['00220656']], '内蒙古自治区烟草公司二连浩特市公司': [['2017-03-09'], 143860.04, '壹拾肆万叁千捌百陆拾元零肆分', ['00220703']], '内蒙古自治区烟草公司锡林郭勒盟公司': [['2017-03-09'], 746301.99, '柒拾肆万陆千叁百零壹元玖角玖分', ['00220652', '00220653']], '内蒙古自治区烟草公司呼和浩特市公司': [['2017-03-09'], 1588156.36, '壹百伍拾捌万捌千壹百伍拾陆元叁角陆分', ['00220721']], '内蒙古自治区烟草公司阿拉善盟公司': [['2017-03-09'], 363738.38, '叁拾陆万叁千柒百叁拾捌元叁角柒分', ['00220649', '00220650']], '广西壮族自治区烟草公司防城港市公司': [['2017-03-09'], 221375.11, '贰拾贰万壹千叁百柒拾伍元壹角壹分', ['00220695']], '黑龙江省烟草公司鹤岗市公司': [['2017-03-09'], 159800.36, '壹拾伍万玖千捌百元叁角伍分', ['00220647']], '中国烟草总公司深圳市公司': [['2017-03-09'], 5480008.56, '伍百肆拾捌万零捌元伍角陆分', ['00220669', '00220672']], '内蒙古自治区烟草公司满洲里市公司': [['2017-03-09'], 488733.39, '肆拾捌万捌千柒百叁拾叁元叁角玖分', ['00220663', '00220664']], '山东潍坊烟草有限公司': [['2017-03-09'], 3720860.15, '叁百柒拾贰万零捌百陆拾元壹角肆分', ['00220658']], '广西壮族自治区烟草公司崇左市公司': [['2017-03-09'], 221375.11, '贰拾贰万壹千叁百柒拾伍元壹角壹分', ['00220694']], '辽宁省烟草公司锦州市公司': [['2017-03-09'], 338773.5, '叁拾叁万捌千柒百柒拾叁元伍角整', ['00220707']], '中国烟草总公司西藏自治区公司': [['2017-03-09'], 1987221.6, '壹百玖拾捌万柒千贰百贰拾壹元陆角整', ['00220673']], '浙江省烟草公司宁波市公司': [['2017-03-09'], 487275.75, '肆拾捌万柒千贰百柒拾伍元柒角伍分', ['00220686']], '山西省烟草公司忻州市公司': [['2017-03-09'], 3239424.45, '叁百贰拾叁万玖千肆百贰拾肆元肆角伍分', ['00220708']], '广西壮族自治区烟草公司贺州市公司': [['2017-03-09'], 553151.43, '伍拾伍万叁千壹百伍拾壹元肆角叁分', ['00220654', '00220696']], '广东烟草阳江市有限责任公司': [['2017-03-09'], 669348.23, '陆拾陆万玖千叁百肆拾捌元贰角贰分', ['00220689', '00220690']], '山西省烟草公司长治市公司': [['2017-03-09'], 4065320.84, '肆百零陆万伍千叁百贰拾元捌角肆分', ['00220665', '00220667']], '山西省烟草公司晋中市公司': [['2017-03-09'], 2738203.36, '贰百柒拾叁万捌千贰百零叁元叁角伍分', ['00220639']], '山东烟台烟草有限公司': [['2017-03-09'], 55200.01, '伍万伍千贰百元零壹分', ['00220659']], '内蒙古自治区烟草公司赤峰市公司': [['2017-03-09'], 1608236.19, '壹百陆拾万捌千贰百叁拾陆元壹角玖分', ['00220651']], '吉林省烟草公司松原市公司': [['2017-03-09'], 986883.77, '玖拾捌万陆千捌百捌拾叁元柒角陆分', ['00220641', '00220642']], '河北省烟草公司唐山市公司': [['2017-03-09'], 1224181.24, '壹百贰拾贰万肆千壹百捌拾壹元贰角叁分', ['00220674']], '山西省烟草公司临汾市公司': [['2017-03-09'], 1731587.83, '壹百柒拾叁万壹千伍百捌拾柒元捌角叁分', ['00220675', '00220676']], '江苏省烟草公司宿迁市公司': [['2017-03-09'], 221375.11, '贰拾贰万壹千叁百柒拾伍元壹角壹分', ['00220638']]}
    # response = JsonResponse(json_info)
    json_file = json.dumps(json_info)
    return render(request, 'autoPrint/index.html', {'json_file':json_file})


def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(base_url=file_config['base_url'], location=file_config['location'])
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename).lstrip('/')
        raw_info = accessExcelData(uploaded_file_url)
        sales_info = mergeDictsValue(raw_info)
        try:
            for k, v in sales_info.items():
                sale_report = SaleReport(payment_comp=k, date=','.join(v[0]), total_price=v[1], total_price_ch=v[2],
                                         tax_receipt=','.join(v[3]), receipt_amount=len(v[3]))
                sale_report.save()
                logger.debug('{comp_name}信息：{list}'.format(comp_name=k, list=str(v)))
            logger.info('日报信息提取完毕！')
            return render(request, 'autoPrint/index.html', {'sales_info': sales_info, 'amount': len(sales_info)})
        finally:
            os.remove(uploaded_file_url)
    else:
        return render(request, 'autoPrint/upload.html')


def details(request, comp_name, order):
    if request.method == 'POST':
        # 付款人信息
        payment_comp = request.POST['pay_name']
        pay_company_account = request.POST['pay_account']
        pay_company_address = request.POST['pay_address']
        pay_account_location = request.POST['pay_location']
        pay = PayCompany.objects.filter(company_name=payment_comp)
        if len(pay) == 0:
            p1 = PayCompany(company_account=pay_company_account, company_address=pay_company_address,
                            account_location=pay_account_location)
            p1.save()
        else:
            pass
        # 收款人信息
        payee_comp = request.POST['payee_name']
        payee_company_account = request.POST['payee_account']
        payee_company_address = request.POST['payee_address']
        payee_account_location = request.POST['payee_location']
        payee_note = request.POST['note']
        payee = PayeeCompany.objects.filter(company_name=payee_comp)
        payee.update(company_account=payee_company_account, company_address=payee_company_address,
                     account_location=payee_account_location, note=payee_note)

        return render(request, 'autoPrint/index.html')
    else:
        pay_list = PayCompany.objects.filter(company_name=comp_name)
        sales_list = SaleReport.objects.filter(payment_comp=comp_name).order_by('added_date')
        payee_list = PayeeCompany.objects.all().order_by('added_date')
        if len(payee_list) == 0:
            payee = PayeeCompany()
        else:
            payee = payee_list[::-1][0]
        if len(pay_list) == 0:
            pay = PayeeCompany()
        else:
            pay = payee_list[::-1][0]
        if len(sales_list) == 0:
            sales = SaleReport()
        else:
            sales = sales_list[::-1][0]
        return render(request, 'autoPrint/details.html', {'pay': pay, 'order': order,
                                                          'payee': payee, 'sales': sales})




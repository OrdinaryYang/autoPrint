import xlrd
import csv
import zipfile
import os
from datetime import datetime
from collections import OrderedDict
from ..config.myconfig import zip_file_config


def rmb_upper(value):
    """
    人民币小写转大写
    :param value: int值
    :return: 大写的金额字符串
    """
    map = [u"零", u"壹", u"贰", u"叁", u"肆", u"伍", u"陆", u"柒", u"捌", u"玖"]
    unit = [u"分", u"角", u"元", u"拾", u"百", u"千", u"万", u"拾", u"百", u"千", u"亿",
            u"拾", u"百", u"千", u"万", u"拾", u"百", u"千", u"兆"]

    nums = []  # 取出每一位数字，整数用字符方式转换避大数出现误差
    for i in range(len(unit) - 3, -3, -1):
        if value >= 10 ** i or i < 1:
            nums.append(int(round(value / (10 ** i), 2)) % 10)

    words = []
    zflag = 0  # 标记连续0次数，以删除万字，或适时插入零字
    start = len(nums) - 3
    for i in range(start, -3, -1):  # 使i对应实际位数，负数为角分
        if 0 != nums[start - i] or len(words) == 0:
            if zflag:
                words.append(map[0])
                zflag = 0
            words.append(map[nums[start - i]])
            words.append(unit[i + 2])
        elif 0 == i or (0 == i % 4 and zflag < 3):  # 控制‘万/元’
            words.append(unit[i + 2])
            zflag = 0
        else:
            zflag += 1

    if words[-1] != unit[0]:  # 结尾非‘分’补整字
        words.append(u"整")
    return ''.join(words)


def accessExcelData(file_dir):
    data = xlrd.open_workbook(file_dir)
    table = data.sheets()[0]
    nrows = table.nrows
    column_name = table.row_values(1)

    pos_date = column_name.index('制单日期')
    pos_payment_comp = column_name.index('调入单位')   # 以此为key简历dict
    pos_total_price = column_name.index('价税合计')
    pos_tax_receipt = column_name.index('发票号')

    # dicts按照以下模式
    # dicts = {'某公司':
    #                   [
    #                     ['时间1', '价税合计1', '发票1'],
    #                     ['时间2', '价税合计2', '发票2']
    #                   ]
    #     }
    dicts = OrderedDict()
    last_payment_comp = ''
    last_date = ''
    for i in range(2, nrows-1):
        payment_comp = table.row_values(i)[pos_payment_comp]
        if payment_comp == '':
            payment_comp = last_payment_comp
        else:
            last_payment_comp = payment_comp
        date = table.row_values(i)[pos_date]
        if date == '':
            date = last_date
        else:
            last_date = date
        total_price = table.row_values(i)[pos_total_price]
        tax_receipt = table.row_values(i)[pos_tax_receipt]
        if payment_comp not in dicts.keys():
            dicts[payment_comp] = [[date, total_price, tax_receipt], ]
        else:
            dicts[payment_comp].append([date, total_price, tax_receipt])
    return dicts


def mergeDictsValue(dicts):
    """
    将dicts中的同类项合并
    :param dicts: 一个OrderedDict
    :return:
    """
    for k, v in dicts.items():
        total_price = 0
        tax_list = []
        date_list = []
        for item in v:
            total_price += item[1]
            if item[2] not in tax_list:
                tax_list.append(item[2])
            if item[0] not in date_list:
                date_list.append(item[0])
        rmb_ch = rmb_upper(total_price)
        dicts[k] = [date_list, total_price.__round__(2), rmb_ch, tax_list]
    return dicts


def write2csv(file_dir, lists, mode='a'):

    csv_file = open(file_dir, mode, newline='')
    writer = csv.writer(csv_file)
    for line in lists:
            writer.writerow(line)
    csv_file.close()


def getToday():
    return datetime.now().strftime('%Y-%m-%d')


def myCompress(dir_path, file_name):
    f = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
    for file in os.listdir(dir_path):
        a, b = file.split('.')
        if b == 'csv':
            file_path = zip_file_config['dir_path'] + file
            f.write(file_path)
    f.close()

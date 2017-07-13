file_config = {
    'base_url': 'media/tmp/',
    'location': 'media/tmp/',
    'csv_dir': 'media/csvFiles/total_info.csv',
    'line': ['0:年_小写', '1:月_小写', '2:日_小写', '3:单位名称_己方', '4:帐号_己方', '5:单位名称_对方', '6:帐号_对方',
             '7:款项用途', '8:开户行_对方', '9:金额_大写', '10:￥金额_小写', '11:输入框', '12:输入框', '13:输入框',
             '16:开户行_己方', '17:省份_己方', '18:地市_己方', '19:省份_对方', '20:地市_对方', '21:输入框'],
    }

acc_file_config = {
    'acc_file_dir': 'media/csvFiles/account.csv',
    'account_line': ['发出日期', '付款人全称', '付款人开户行', '金额', '托收票据名称', '附寄单证张数', '付款标注']
}

zip_file_config = {
    'file_name': 'media/csvFiles/download.zip',
    'dir_path': 'media/csvFiles/'
}

ems_file_config = {
    'ems_file_dir': 'media/csvFiles/ems.csv',
    'ems_line': ['0:单位名称_己方', '1:地址_己方', '2:单位名称_对方', '3:地址_对方'],
    'company_from': '上海浦东发展银行',
    'company_from_addr': '郑州市金水区金水路299号',
}
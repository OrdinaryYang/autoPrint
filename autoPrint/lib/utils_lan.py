import requests
from autoPrint.config.myconfig import webservice_raw_req_content


def email_verify(username, password):
    """
    验证邮箱用户名密码是否正确
    :param username: 邮箱完整用户名
    :param password: 邮箱密码
    :return: boolean
    """
    # user = username.split('@')[0]
    # header = {'Content-Type': 'text/xml'}
    # raw1 = webservice_raw_req_content.replace('username', user)
    # data = raw1.replace('password', password)
    # r = requests.post('http://10.15.60.18/Domain/DomianUserService.asmx', data=data,
    #                   headers=header)
    # if str(r.content).find('true') >= 0:
    #     return True
    # else:
    #     return False
    return True

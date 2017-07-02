# -*- coding: utf-8 -*-

'''
本程序用于福泉行处理消费代扣业务逻辑
'''
import base64
import datetime
import json
import logging
import os
import sys

import pyDes
import requests

scheme = 'http://'
target_ip = '114.55.250.229'
port_no = ':90'
app_name = '/LbswWebService'
bank_name = '富民银行'


class DES:
    # IV必须是 8 字节长度的十六进制数
    iv = 'F8A3E9A5'
    # key加密密钥长度，24字节
    key = 'bRs5oXHF7tg=bRs5oXHF7tg='

    def __init__(self, key):
        self.key = key

    # 加密方法
    def encrypt(self, data):
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        d = k.encrypt(data)
        d2 = base64.encodebytes(d)
        d3 = str(d2, encoding='utf-8')
        return d3

    # 解密方法
    def decrypt(self, data):
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data2 = base64.decodebytes(data)
        d = k.decrypt(data2)
        d2 = str(d, encoding='utf-8')
        return d2


# 缴费调用函数
def payment_call_func(url, period, usercode, name, account, water_rate, sewage_rate, fine, result):
    # 构造传输数据结构
    ret_val = {"Period": period, "UserCode": usercode, "AccountName": name, \
               "BankAccount": account, "WaterRate": water_rate, "SewageRate": sewage_rate, \
               "OverdueFine": fine, "Result": result}
    print(str(ret_val))
    pass


# 程序索引页面
def show_biz_interface():
    indexStr = '''    ---------------福泉水费处理--------------------
    使用本工具处理业务逻辑数据，请选择合适的选项：
    [00]检查网络是否可达
    [10]单个操作：查询客户欠费信息
    [11]单个操作：上传客户签约信息
    [12]单个操作：回写客户缴费信息
    [20]批量操作：查询本行客户欠费信息
    [21]批量操作：批量上传客户签约数据
    [22]批量操作：批量下载签约客户欠费数据
    [23]批量操作：将批扣结果同步更新至服务器
    [30]对账操作：上传对账结果
    [99]退出程序
    ------------------------------------------------
    '''
    t = os.system('clear')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(indexStr)


# 00代码 测试网络是否可达
def check_connection():
    print('\t开始测试网络连通性')
    ret_val = os.system('ping -c 2 -W 1 %s' % target_ip)
    if ret_val:
        print('--连接失败')
    else:
        print('--网络可达')
    input('请按任意键继续...')


# 99代码 退出程序的运行
def quit_command():
    try:
        sys.exit(0)
    except:
        print('--- 程序即将退出 ---')
    finally:
        print('--- BYE ---')
        os._exit(0)


# 11代码 单个上传客户签约信息
def upload_client_sign_info():
    pass


# 12代码 回写客户缴费信息
def sync_client_payment_info():
    # 缴费对应的API
    api_name = 'SaveResultRecord'

    # 对应的API地址
    url = '{0}{1}{2}{3}{4}'.format(scheme, target_ip, port_no, app_name, api_name)
    logging.info(url)

    # 从输入构造结构体
    period = input('请输入客户缴费月份：')
    name = input('请输入客户姓名：')


# 22代码 批量下载客户欠费信息
def get_all_clients_info():
    # 调用的API名
    api_name = '/GetOweRecord'

    # 对应的API地址
    url = '{0}{1}{2}{3}{4}'.format(scheme, target_ip, port_no, app_name, api_name)
    logging.info(url)

    # 输入起止月份
    query_from = input('请输入开始月份（201701）：')
    query_to = input('请输入截止月份（201701）：')

    # 构造数据结构，并将单引号转化为双引号，以便服务器顺利解析
    src_struct = {'BankName': bank_name, 'PeriodFrom': query_from, 'PeriodTo': query_to}
    src_str = str(src_struct)
    src_str = src_str.replace("'", '"')

    # 由API对应的KEY实例DES对象
    des = DES('bRs5oXHF7tg=bRs5oXHF7tg=')

    # 将构结数据（JSON格式）编码为UTF8
    encryptdata = des.encrypt(src_str.encode('utf-8'))
    encryptdata = encryptdata.replace('\n', '')

    logging.info('加密后的数据是: %s ' % (encryptdata))

    # 生成传输用到的POST数据
    crypto_res = {'Result': encryptdata}
    result = requests.post(url, data=crypto_res)

    logging.info(crypto_res)

    # 把调用结果转化为json对象
    res_jo = json.loads(result.text)

    # 记录json对象的msg消息
    logging.info('Return Msg: %s' % res_jo['msg'])

    res_list = res_jo['detail']

    for per in res_list:
        print('账号：%s' % per['账号'])
    input('请按任意键继续...')


option_func = {'00': check_connection, '12': sync_client_payment_info, '22': get_all_clients_info, '99': quit_command}

if __name__ == '__main__':
    logging.basicConfig(filename='./fqsw.log', level=logging.DEBUG, \
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', \
                        filemode='a')
    while True:
        show_biz_interface()
        option = input('请输入操作代码：')
        print('您选择的是:{}'.format(option))
        if option in option_func.keys():
            func_name = option_func[option]
            func_name()

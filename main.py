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

    def __init__(self,key):
        self.key = key

    def encrypt(self, data):
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        d = k.encrypt(data)
        d2 = base64.encodebytes(d)
        d3 = str(d2, encoding='utf-8')
        return d3

    def decrypt(self, data):
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data2 = base64.decodebytes(data)
        d = k.decrypt(data2)
        d2 = str(d,encoding='utf-8')
        return d2


# 程序索引页面
def show_biz_interface():
    indexStr = '''    ---------------福泉水费处理--------------------
    使用本工具处理业务逻辑数据，请选择合适的选项：
    [00]检查网络是否可达
    [10]单个操作：查询客户欠费信息
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


# 22代码 批量下载客户欠费信息
def get_all_clients_info():
    api_name = '/GetOweRecord'
    url = '{0}{1}{2}{3}{4}'.format(scheme, target_ip, port_no, app_name, api_name)
    logging.info(url)
    query_from = input('请输入开始月份（201701）：')
    query_to = input('请输入截止月份（201701）：')
    # 构造数据结构
    src_struct = {'BankName': bank_name, 'PeriodFrom': query_from, 'PeriodTo': query_to}
    src_str = str(src_struct)
    src_str = src_str.replace("'",'"')
    des = DES('bRs5oXHF7tg=bRs5oXHF7tg=')
    encryptdata = des.encrypt(src_str.encode('utf-8'))
    encryptdata = encryptdata.replace('\n','')
    print('加密后的数据是: %s ' % (encryptdata))
    crypto_res = {'Result':encryptdata}
    result = requests.post(url, data=crypto_res)
    logging.info(crypto_res)
    print('结果 %s' % result.text)
    res_jo = json.loads(result.text)
    #TODO: 等待水务端处理API异常
    logging.info('Return Msg: %s' % res_jo['msg'])
    res_list = res_jo['detail']
    for per in res_list:
        print('账号：%s' % per['账号'])
    input('请按任意键继续...')


option_func = {'00': check_connection, '22': get_all_clients_info, '99': quit_command}

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

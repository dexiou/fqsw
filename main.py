# -*- coding: utf-8 -*-

'''
本程序用于福泉行处理消费代扣业务逻辑
'''
import datetime
import os
import sys
import requests
import logging
import json

scheme = 'http://'
target_ip = '114.55.250.229'
port_no = ':90'
app_name = '/LbswWebService'
bank_name = '富民银行'


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
    query_from = input('请输入开始月份（201705）：')
    query_to = input('请输入截止月份（201705）：')
    # 构造数据结构
    dt = {'BankName': bank_name, 'PeriodFrom': query_from, 'PeriodTo': query_to}
    result = requests.post(url, data=dt)
    logging.debug(result.text)
    res_jo = json.loads(result.text)
    print(res_jo.msg)
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

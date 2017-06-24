# -*- coding: utf-8 -*-

'''
本程序用于福泉行处理消费代扣业务逻辑
'''
import datetime
import os

scheme = 'http://'
target_ip = '114.55.250.229'
port_no = '90'
app_name = 'LbswWebService'


def showBizInterface():
    indexStr = '''
    ------------------------------------------------
    使用本工具处理业务逻辑数据，请选择合适的选项：
    [00]检查网络是否可达
    [10]单个操作：查询客户欠费信息
    [20]批量操作：查询本行客户欠费信息
    [21]批量操作：批量上传客户签约数据
    [21]批量操作：批量下载签约客户欠费数据
    [22]批量操作：将批扣结果同步更新至服务器
    [30]对账操作：上传对账结果
    ------------------------------------------------
    '''
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(indexStr)


def check_connection():
    print('\t开始测试网络连通性')
    ret_val = os.system('ping -c 2 -W 1 %s' % target_ip)
    if ret_val:
        print('--连接失败')
    else:
        print('--网络可达')


option_func = {'00': check_connection}

if __name__ == '__main__':
    showBizInterface()
    option = input('请输入操作代码：')
    print('您选择的是:{}'.format(option))
    if option in option_func.keys():
        func_name = option_func[option]
        func_name()

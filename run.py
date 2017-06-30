# -*- coding: utf-8 -*-
# @Author: dexiou
# @Date:   2017-05-31 20:42:29
# @Last Modified by:   anchen
# @Last Modified time: 2017-06-01 17:48:59
import sys
import os
import logging
import xlrd
import xlwt
import time

# 接受的文件类型。xlsx 和 xls
Const_EXCEL_Format = [".xls",".xlsx"]

# 所有的简历清单
resume_list = []

# 简历信息列表（供写入使用）
resume_info_list = []

# 信息列表
Const_Sheet_Info = ['姓名','性别','籍贯','民族','出生日期','身高','身份证号','婚姻状况','户口','政治面貌','专业特长','健康状况','参加工作时间','手机号码','家庭住址','应聘岗位','应聘地区','调配意愿','毕业生状态','文件位置']
# 属性列表
Const_Attr_Info = ['xm','xb','jg','mz','csrq','sg','sfzh','hyzk','hk','zzmm','zytc','jkzk','cjgzsj','sjhm','jtzz','ypgw','ypdq','tpyy','byszt','filepath']

# 根据传入的root目录，找到所有的xlsx简历
def get_resume_dir(root):
    # 仅walk就可以完成递归
    for rt, dirs, files in os.walk(root):
        for f in files:
            fname = os.path.splitext(f)
            if fname[1] in Const_EXCEL_Format:
                resume_list.append(os.path.join(rt,f))


# 处理简历
def retrive_resume_info(resumefile):
    logging.info('resumefile is %s' % resumefile )
    ri = ResumeInfo()
    try:
        data = xlrd.open_workbook(resumefile)
        table = data.sheet_by_index(0)
        # 取姓名
        ri.xm = table.cell(2,3).value
        # 取性别
        ri.xb = table.cell(2,5).value
        # 取籍贯
        ri.jg = table.cell(2,7).value
        # 取民族
        ri.mz = table.cell(2,9).value
        # 取出生日期
        ri.csrq = table.cell(2,11).value
        #---------------第一行结束-------------------------------
        # 取身高
        ri.sg = table.cell(3,3).value
        # 取身份证号
        ri.sfzh = table.cell(3,5).value
        # 取婚姻状况
        ri.hyzk = table.cell(3,9).value
        # 取户口
        ri.hk = table.cell(3,11).value
        #---------------第二行结束-------------------------------
        # 取政治面貌
        ri.zzmm = table.cell(4,3).value
        # 取专业特长
        ri.zytc = table.cell(4,5).value
        # 取健康状况
        ri.jkzk = table.cell(4,11).value
        #---------------第三行结束-------------------------------
        # 取参加工作时间
        ri.cjgzsj = table.cell(5,3).value
        # 取手机号码
        ri.sjhm = table.cell(5,5).value
        # 取家庭住址
        ri.jtzz = table.cell(5,8).value
        #---------------第四行结束-------------------------------
        # 取应聘岗位
        ri.ypgw = table.cell(6,3).value
        # 取应聘地区
        ri.ypdq = table.cell(6,7).value
        # 取调配意愿
        ri.tpyy = table.cell(6,9).value
        # 取毕业生状态
        ri.byszt = table.cell(6,11).value
        # 文件地址
        ri.filepath = resumefile

        resume_info_list.append(ri)
    except Exception as e:
        logging.error('Error is %s' % e)


# 写入excel
def createResumeInfoFile(fn='TotalInfo.xls'):
    now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    try:
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('汇总 %s' % now)
        bold_style = xlwt.easyxf('font: bold 1')
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'M/D/YY'
        # 写表头
        for index,info in enumerate(Const_Sheet_Info):
            sheet.write(0, index, info, bold_style)
        # 须妥善处理日期类型的数据
        for i, ri in enumerate(resume_info_list):
            for j,info in enumerate(Const_Attr_Info):
                if hasattr(ri, info):
                    value = getattr(ri, info)
                    if info=='filepath':
                        v = 'HYPERLINK("file://%s";"%s")' % (value, value)
                        sheet.write(i+1, j, xlwt.Formula(v))
                    elif info=='csrq':
                        sheet.write(i+1, j, value, date_style)
                    elif info=='cjgzsj':
                        sheet.write(i+1, j, value, date_style)
                    else:
                        sheet.write(i+1, j, value)

        workbook.save(fn)

    except Exception as e:
        logging.error(' Writing excel file error %s' % e)


# 定义存放简历信息的类
class ResumeInfo(object):
    pass

# 主函数入口
if __name__ == '__main__':
    # 设置日志
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s [line:%(lineno)4d] %(levelname)8s:%(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='run.log',
                filemode='w')

    if len(sys.argv)>=2 :
        root = sys.argv[1]
    else:
        root = os.getcwd()

    get_resume_dir(root)
    logging.info('Total %d resume(s) found' %  len(resume_list))


    for filename in resume_list:
        retrive_resume_info(filename)

    createResumeInfoFile()

    os.system('pause')
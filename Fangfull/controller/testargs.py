# -*- coding:utf-8 -*-
#!/usr/bin/python
from Fangfull.common import readxls,writexls
import time
import threading
import re
import pprint
import csv


# 读取excel
## xls 路径，标签页名称，第几列
def get_readxls(xlsname,sheelname,*args):
    print('开始读表')
    my_readxls = readxls.Readxls(xlsname)
    table = my_readxls.readsheet(sheelname)
    table_heard = my_readxls.cell_value_AppointNrows(table,0)
    table_message,array_ncols,is_write = my_readxls.cell_value_AppointNcols(table,*args)
    print("读表完成")
    return table_heard,table_message,array_ncols,is_write

##需要比较的字段进行组合拼接
def get_listmerge(List):
    print('拼接字符串')
    list_cols_max = []
    for i in range(len(List)):
        list_cols_max.append(len(List[i]))
    cols_max = max(list_cols_max)
    is_true = True
    count = 0
    str_merge = []
    while(is_true):
        if count <  cols_max:
            str_type = ''
            for i in range (len(List)):
                if str_type == '':
                    str_type = str(List[i][count])
                else:
                    str_type = str_type +'&&'+ str(List[i][count])
            str_merge.append(str_type)
            count +=1
        else:
            is_true = False
    print('拼接字符串完成')
    return str_merge

## 统计两个list 中每个元素重复出现的次数
def statistics(message,is_write):
    print("开始统计重复次数")
    type_message = set(message)
    type_listmessage = list(type_message)
    type_listcount = []
    print(len(message))
    print(len(is_write),is_write)
    for i in range(len(type_listmessage)):
        count = 0
        for j in range(len(message)):
            if str(type_listmessage[i]) == str(message[j]):
                count = count+1
                if count > 1:
                    is_write[j] = False
        type_listcount.append(count)

        # print(type_listmessage[i],count)
    # print(len(message),len(is_write),len(type_listcount))
    print(is_write)
    print("重复次数统计完成")

    return is_write,type_listcount
    # for i in range(len(message)):
    #     print(message[i],is_write[i],'  ',type_listcount[i])


def get_split(listMessage):
    message = []
    for i in range(len(listMessage)):
        message.append(listMessage[i].split("&&"))
    return message

def get_choose(message,choose):
    typemessage = []
    for i in range(len(message)):
        typemessage.append(message[i][choose-1])

    myset = set(typemessage)
    for item in myset:
        print(item,'   ',typemessage.count(item))

def openxls():
    rwxls = writexls.Writexls()
    rwxls.add_sheet('test1')
    return rwxls
def rwxls(xlsname,table_message,is_write,listcount,table_heard,write_xls):
    rwxls = openxls()
    # nrows 行 ncols 列
    nrows = 0
    ncols = 0
    print("开始写入xls")
    type_table = []
    type_table_heard = []
    for i in range (len(table_message)):
        type_table_ncols = []
        if i+1 in write_xls:
            for j in range (len(table_message[i])):
                if is_write[j]:
                    type_table_ncols.append(str(table_message[i][j]))
                    nrows +=1
            type_table_heard.append(table_heard[i])
            nrows = 0
            ncols+=1
            type_table.append(type_table_ncols)
    type_table.append(listcount)

    for i in range(len(type_table_heard)):
        rwxls.xls_write_byone(0,i,str(type_table_heard[i]))


    for i in range(len(type_table)):
        for j in range(len(type_table[i])):
            rwxls.xls_write_byone(j+1,i,str(type_table[i][j]))
    print("写入完成")
    timenew = str(time.strftime('%Y-%m-%d_%H_%M_%S',time.localtime(time.time())))
    rwxls.save_xls(str(xlsname)+str(timenew)+'.xls')

#list 筛除重复返回list
def Thread_listset(list_message):
    type_message = set(list_message)
    return list(type_message)

def Thread_staristics(value,list_all,is_write):
    print("开始统计重复次数")
    count = 0
    for i in range (len(list_all)):
        if value == list_all[i]:
            count +=1
            if count > 1:
                is_write[i] = False
    return count,is_write
class Thread_run(threading.Thread):
    def __init__(self,table_heard,table_message,ncols_message,is_write):
        threading.Thread.__init__(self)
        self.table_heard = table_heard
        self.table_message = table_message
        self.ncols_message = ncols_message
        self.is_write = is_write
    def run(self):
        listmerge = get_listmerge(self.ncols_message)
        print(len(listmerge))
        listmerge_set = Thread_listset(listmerge)
        print(len(listmerge_set))
        for i in range(len(listmerge_set)):
            count,is_write = Thread_staristics(listmerge_set[i],listmerge,self.is_write)
            print(count)
        print(is_write)

        # print(listmerge_set)
        # is_write,type_listcount = statistics(listmerge,self.is_write)  ## 统计两个list 中每个元素重复出现的次数
        # write_xls = [1,2,3,4]
        # xlsname = 'test'
        # rwxls(xlsname,self.table_message,is_write,type_listcount,self.table_heard,write_xls)


if __name__ == '__main__':
    # xlsname = "D:\Backup\桌面\全部-订单明细2016-1-7.xlsx"
    # sheelname = '订单明细2016'
    # xlsname = "D:\Backup\桌面\XXYY.xlsx"
    # sheelname = 'Sheet1'
    # nrows_one = 2
    # nrows_two = 4
    # table_heard,table_message,ncols_message,is_write = get_readxls(xlsname,sheelname,nrows_one,nrows_two)
    # listmerge = get_listmerge(ncols_message)
    # is_write,type_listcount = statistics(listmerge,is_write)
    # write_xls = [1,2,3,4]
    # xlsname = 'test'
    # rwxls(xlsname,table_message,is_write,type_listcount,table_heard,write_xls)

    # xlsname = "D:\Backup\桌面\XXYY.xlsx"
    # sheelname = 'Sheet1'
    # nrows_one = 2
    # nrows_two = 4
    #
    # table_heard,table_message,ncols_message,is_write = get_readxls(xlsname,sheelname,nrows_one,nrows_two)
    # t = Thread_run(table_heard,table_message,ncols_message,is_write)
    # t.start()





    import codecs
    FileL = open('D:\Backup\桌面\XXYY.csv',"r")
    reader = csv.reader(FileL)
    for line in reader:
        print(line)


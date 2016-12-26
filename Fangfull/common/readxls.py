# -*- coding:utf-8 -*-
#!/usr/bin/python

import xlrd
import pprint
import time
from xlrd import xldate_as_tuple
class Readxls:
    def __init__(self,Filename):
        self.openbook = xlrd.open_workbook(Filename,'rw')

    def readsheet(self,indexName):
        sheetName = range(self.openbook.nsheets)
        for i in range(0,len(sheetName)):
            if indexName == self.openbook.sheet_by_index(i).name :
                table = self.openbook.sheet_by_index(i)
                return table
            else:
                return None

    def cell_value(self,table):
        nrows = table.nrows  # 行
        ncols = table.ncols  # 列
        array_nrows = []
        array_table = []
        for cols in range(0,ncols):
            for rows in range(0,nrows):
                # print type(table.cell(rows,cols).value)
                # if type(table.cell(rows,cols).value) != str:
                #     table.cell(rows,cols).value = str(table.cell(rows,cols).value)
                # array_nrows.append(table.cell(rows,cols).value)
                array_nrows.append(str(table.cell(rows,cols).value))

            array_table.append(array_nrows)


        return array_table

    # 返回某一列下的所有数据
    def cell_value_AppointNcols(self,table,*getnrows):
        nrows = table.nrows  # 行
        ncols = table.ncols  # 列
        table_ncols = [[] for row in range(len(getnrows))] #接收某列下的内容
        tableheards = []
        # print(str(table.cell(0,1).value))
        data = []
        for cols in range(0,ncols):
            tableheards.append(str(table.cell(0,cols).value))
            data.append(True)
            if '日' in tableheards[cols] or '时间' in tableheards[cols]:
                data.append(False)
        table_message = []
        is_write = [True]*(nrows-1)  #[[True] * ncols for row in range(nrows)]  #是否写入


        for cols in range(ncols):
            table_message_type = []
            for rows in range(1,nrows):
                # time.strptime(str, "%Y/%m/%d %H:%M:%S")
                # if data[cols] == True:
                # else:
                table_message_type.append(str(table.cell(rows,cols).value))
                for i in range(0,len(getnrows)):
                    if cols == getnrows[i]-1:
                        table_ncols[i].append(str(table.cell(rows,cols).value))

            table_message.append(table_message_type)
        return table_message,table_ncols,is_write
        # 返回某一列下的所有数据
    def cell_value_AppointNcols_one(self,table,getnrows):
        nrows = table.nrows  # 行
        ncols = table.ncols  # 列
        array_ncols = [] #接收某列下的内容
        tableheards = []
        print(getnrows)
        for cols in range(getnrows-1,getnrows):
            tableheards.append(str(table.cell(0,cols).value))

        for cols in range(getnrows-1,getnrows):
            for rows in range(1,nrows):
                array_ncols.append(str(table.cell(rows,cols).value))
        print(array_ncols)
        return array_ncols



        # 返回某一行下的所有数据
    def cell_value_AppointNrows(self,table,getncols):
        ncols = table.ncols  # 列
        array_nrows = [] #接收某列下的内容
        for cols in range(0,ncols):
            for rows in range(getncols,getncols+1):
                array_nrows.append(str(table.cell(rows,cols).value))
        return array_nrows


    ## 返回行总数
    def get_nrows(self,table):
        return table.nrows

    ## 返回列总数
    def get_ncols(self,table):
        return table.ncols

    #获取excel 中的所有数据，返回一个二维数组
    def gettable_rowAndcol(self,table):
        nrows = table.nrows  # 行
        ncols = table.ncols  # 列
        tablearray = []
        for i in range(nrows):
            rows = []
            for j in range (ncols):
                rows.append(str(table.cell(i,j).value))
            tablearray.append(rows)
        return tablearray

    def cell_value_AppointNcols_complex(self,table,*args):
        nrows = table.nrows  # 行
        array_ncols = [] #接收某列下的内容
        print(args,len(args))
        # for i in range()
        # for cols in range(getnrows,getnrows+1):
        #     for rows in range(0,nrows):
        #         array_ncols.append(str(table.cell(rows,cols).value))
        return array_ncols


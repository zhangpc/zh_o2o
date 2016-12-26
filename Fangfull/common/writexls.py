# -*- coding:utf-8 -*-
#!/usr/bin/python
import xlwt,time

class Writexls():
    def __init__(self):
        print("创建xls")
        self.workbook = xlwt.Workbook(encoding = 'utf-8')

    def add_sheet(self,sheetname):
        print("在xls创建sheet")
        self.worksheet = self.workbook.add_sheet(sheetname)
        # font = xlwt.Font() # Create the Font
        # font.name = 'Times New Roman'
        # font.bold = True
        # font.underline = True
        # font.italic = True
        # style = xlwt.XFStyle() # Create the Style
        # style.font = font # Apply the Font to the Style

    # # nrows   # 行
    # # ncols  # 列
    def xls_write(self,*args):
        print(args)
        for i in range(len(args)):
            print(args[i])


    def xls_write_array(self,*args):
        print("写入xls")
        print(args)
        for i in range(1,len(args)):
            for j in range(0,len(args[i])):
                self.worksheet.write(j,i,str(args[i][j]))
        print("xls写入完成")

    ## 指定写入行
    def xls_write_nrows(self,nrows,*args):
        for i in range(len(args)):
            self.worksheet.write(nrows,i,str(args[i]))

    def save_xls(self,xlsname):
        print("保存xls")
        self.workbook.save(str(xlsname))
        print('xls保存成功')

    #逐个写入  nrows 行 ncols 列
    def xls_write_byone(self,nrows,ncols,args):
        self.worksheet.write(nrows,ncols,str(args))


if __name__ == '__main__':

    # phone = [1,2,3,4]
    # phone1 = [11,22,33,44]
    # phone2 = [13,23,33,43]
    # phone3 = [14,24,34,44]
    # # phone = [15,25,35,45]
    #
    rw = Writexls()
    # rw.add_sheet('test1')
    # rw.xls_write(phone,phone1,phone2,phone3)
    # rw.save_xls('111.xls')


    phone = '1'

    rw = Writexls
    for i in range(3):
        rw.xls_write(0,i,phone)
    rw.save_xls('1112.xls')
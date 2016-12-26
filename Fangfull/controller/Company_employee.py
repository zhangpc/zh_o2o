# -*- coding:utf-8 -*-
#!/usr/bin/python

import tools_request
from Fangfull.controller import User_login
from config import Config
import tools_mysql

# 内部用户
def create_Employee(ipblue,cookies):

    url = str(ipblue)+"admin.php?r=product/companyEmployee/create"
    data = {
            'CompanyEmployee[name]':'asdf',
            'CompanyEmployee[sex]':'1',
            'CompanyEmployee[superior]':'2093',
            'CompanyEmployee[company_id]':'2',
            'CompanyEmployee[depart_id]':'1187',
            'CompanyEmployee[username]':'test00002',
            'CompanyEmployee[password]':'123456',
            'CompanyEmployee[title]':'',
            'CompanyEmployee[mobile]':'13683300010',
            'CompanyEmployee[email]':'ztx1501@sina.com',
            'CompanyEmployee[status]':'1',
            'CompanyEmployeeRole[id]':'4',
             }
    print (cookies)
    tools_request.post_Request(url,data,cookies = cookies)

#通过内部用户登录用户名查询ID和角色名称
def sql_Employee_UserMessage(CompanyEmployee_username,sql_connect):
    employee_id,employee_name=tools_mysql.MysqlConnect('select id,name from erp_company_employee where username = '+'"'+str(CompanyEmployee_username)+'"',sql_connect)[0]
    return employee_id,employee_name
if __name__ == "__main__":
    cookies = User_login.admin_login_blue()  #管理员登录
    create_Employee(cookies)    #创建经纪公司
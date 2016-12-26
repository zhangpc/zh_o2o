# -*- coding:utf-8 -*-
#!/usr/bin/python
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
import re
import time
import datetime
import tools_request
from config import Config
from Fangfull.controller import User_login,Customer_visiting_record,Building
import bs4
import tools_mysql
# sql_connect = Config.sql_connect(Config.sql_index).set_connect()

# 报备用户,返回用户id
def add_customer(ipblue,cookies,phone,building_id,building_name,customer_grade,isdele_customer,sql_connect):
    parameter = {
            'para':'',
            'Customer[ids]':'0',
            'building_id':building_id,   #24 北京中弘大厦  # 100中弘广场
            'Customer[customer_name]':'自'+str(phone)+'报备',
            'Customer[customer_cellphone]':phone,
            'grade':str(customer_grade),
            'Customer[customer_sex]':'2',
            'Customer[customer_card]':'522635198708184662',
            'Customer[customer_province]':'16',
            'Customer[customer_city]':'203',
            'Customer[customer_county]':'2027',
            'Customer[customer_address]':'自动化添加',
            'Customer[customer_remark]':'自动化添加',
            'yt0':'保 存',
            }

    url = str(ipblue)+"customer/savecustomer"
    print(phone,building_id,building_name)
    try:
        print("查询客户手机号是否已存在")
        is_phone =tools_mysql.MysqlConnect('select * from customer where customer_cellphone =  '+'"'+str(phone)+'"',sql_connect)[0]
    except:
        print("用户的手机号不存在，可以添加报备")
        is_phone = False

    if is_phone != False:
        print("客户手机号存在")
        if isdele_customer:
            print("准备变更已存在的客户手机号")
            tools_mysql.MysqlConnect('UPDATE customer ct set ct.customer_name = '+'"'+'自动化删除'+str(phone)+'"' + ',ct.customer_cellphone='+'"自动化删除"'+' where ct.customer_cellphone='+'"'+str(phone)+'"',sql_connect)
            print("成功变更已存在的客户手机号")

    print("开始报备用户,手机号码是 ：" + str(phone))
    Content = tools_request.post_Request(url,parameter,cookies=cookies)
    assert_add_customer =  tools_request.Assert('添加成功',Content,1)
    tools_request.re_return_message(Content)
    print("报备成功")
    userid = myOwenCustom(ipblue,cookies,phone,building_name)# 返回用户的手机号和ID
    return userid
#通过手机号查找客户
def myOwenCustom(ipblue,cookies,phone,building_name):
    time.sleep(3)
    parameter = {
        'Customer[customer_id]':'',
        'Customer[customer_name]':'',
        'Customer[customer_cellphone]':str(phone),
        'Customer[grade]':'',
        'Customer[building]':building_name,
        'yt0':'搜 索',
    }
    url = str(ipblue) + 'customer/myOwenCustom'
    Content = tools_request.post_Request(url,parameter,cookies=cookies)
    # print(Content)
    re_userid= re.findall(r'<a href="/customerAppointment/addcreate/id/(\w+)/from/myOwenCustom" class="formNedit">',Content)[0]
    return re_userid



if __name__ == '__main__':

    # ip = Config.Ip()
    # ip.set_Ipblue('http://betawww.fangfull.com/')
    # ip.set_Ipred('http://betawww.fangfull.com/')
    # ip_blue = ip.get_Ipblue()
    # ip_red = ip.get_Ipred()
    #
    # sqlconnect = Config.SqlConnect()
    # sqlMysql = sqlconnect.get_fangfull_beta_sql()
    # zcsxmzj = 'zcsxmzj'
    # zcsacjjy = 'zcsacjjy'
    # zcsachtkf = 'zcsachtkf'
    # customer_phone = '13600006000'
    # broker_cookies = User_login.broker_login(ip_blue,'13800000001')  # 登录经纪人
    # building_name = '中弘西岸首府'#'北京中弘大厦'# 新奇世界-长白水镇4号地 #'新奇世界-长白水镇5号地'
    # building_id = Building.sql_getbuliding_id(building_name,sqlMysql)
    # customer_id = add_customer(ip_blue,broker_cookies,customer_phone,building_id,building_name,sqlMysql)  #给经纪人添加并报备用户,返回用户ID
    # acjjy_cookies = User_login.acgly_login_red(ip_red,zcsacjjy) # 登录案场讲解员账号
    # Customer_visiting_record.customerVisitingRecord(ip_blue,acjjy_cookies,customer_id,customer_phone,False,sqlMysql) #添加用户到访
    #
    # ackf_cookies = User_login.ackf_login_blue(ip_red,zcsachtkf)  #登录案场客服
    # VisitAudit_id = Customer_visiting_record.getVisitAuditList(ip_red,ackf_cookies,customer_phone) # 查询案场客服审核用户时的ID
    # Customer_visiting_record.VisitAudited(ip_red,ackf_cookies,VisitAudit_id)# 到访审核通过


    ip = Config.Ip()
    ip.set_Ipblue('http://test1www.xqshijie.com/')
    ip.set_Ipred('http://test2www.xqshijie.com/')
    ip_blue = ip.get_Ipblue()
    ip_red = ip.get_Ipred()
    sqlconnect = Config.SqlConnect()
    sqlMysql = sqlconnect.get_fangfull_test_sql()

    # ip = Config.Ip()
    # ip.set_Ipblue('http://betawww.fangfull.com/')
    # ip.set_Ipred('http://betaerp.fangfull.com/')
    # ip_blue = ip.get_Ipblue()
    # ip_red = ip.get_Ipred()
    # sqlconnect = Config.SqlConnect()
    # sqlMysql = sqlconnect.get_fangfull_beta_sql()


    # customer_phone = '13717671034'
    # broker_cookies = User_login.broker_login(ip_blue,'18911983251')  # 登录经纪人
    # building_name = '北京中弘大厦'#'北京中弘大厦'# 新奇世界-长白水镇4号地 #'新奇世界-长白水镇5号地'
    # building_id = Building.sql_getbuliding_id(building_name,sqlMysql)
    # customer_id = add_customer(ip_blue,broker_cookies,customer_phone,building_id,building_name,sqlMysql) # 添加客户报备
    #
    # Customer_visiting_record.customerAppointment_savebroker(ip_blue,broker_cookies,customer_id,customer_phone,building_id) # 添加客户预约
    # appointment_status = '1'  ####'状态 1 预约 2确认 3如期履约 4爽约 5取消',
    # appointmentid = Customer_visiting_record.get_myReserveList(ip_blue,broker_cookies,building_id,customer_id,customer_phone,appointment_status,sqlMysql)
    # acjjy_cookies = User_login.acgly_login_blue(ip_red,'zcsacjjy') # 登录案场讲解员（置业顾问）
    # Customer_visiting_record.appointment_status_set(ip_red,acjjy_cookies,appointmentid,'3') #讲解员确认预约，预约状态改变为“3如期履约”
    # Customer_visiting_record.get_myReserveList(ip_blue,broker_cookies,building_id,customer_id,customer_phone,'3',sqlMysql) #经纪人查看预约状态是否正确


    # # '13717671016','13717671017','13717671018','13717671020'
    # customer_phone = '13717671062'
    # customer_id = '1001081'
    # #building_name = '北京御马坊楼盘'
    # building_name = '北京中弘大厦'
    # # building_name = '由山由谷楼盘'
    # #building_name = '济南中弘广场'
    # zcsxmzj = 'zcsxmzj'
    # zcsacjjy = 'zcsacjjy'
    # zcsachtkf = 'zcsachtkf'
    #
    # building_id = Building.sql_getbuliding_id(building_name,sqlMysql)
    # acjjy_cookies = User_login.acgly_login_red(ip_red,zcsacjjy) # 登录案场讲解员账号
    # Customer_visiting_record.customerVisitingRecord(ip_blue,acjjy_cookies,customer_id,customer_phone,True,building_id,building_name,sqlMysql) #添加用户在1小时外到访到访



    ### 下面是经纪公司报备客户的

    customer_phone = '13700000032'
    #building_name = '北京御马坊楼盘'
    building_name = '北京中弘大厦'
    # building_name = '由山由谷楼盘'
    #building_name = '济南中弘广场'

    zcsxmzj = 'zcsxmzj'
    zcsacjjy = 'zcsacjjy'
    zcsachtkf = 'zcsachtkf'

    jigoujinjiren = '13700000100' #机构经纪人账号 密码都是123456
    building_id = Building.sql_getbuliding_id(building_name,sqlMysql)
    broker_cookies = User_login.broker_login(ip_blue,jigoujinjiren)  # 机构登录经纪人


    customer_id = add_customer(ip_blue,broker_cookies,customer_phone,building_id,building_name,True,sqlMysql)  #给经纪人添加并报备用户,返回用户ID

    acjjy_cookies = User_login.acgly_login_red(ip_red,zcsacjjy) # 登录案场讲解员账号
    # Customer_visiting_record.customerVisitingRecord(ip_blue,acjjy_cookies,customer_id,customer_phone,True,building_id,building_name,sqlMysql) #添加用户在1小时内到访，客户归中弘
    Customer_visiting_record.customerVisitingRecord(ip_blue,acjjy_cookies,customer_id,customer_phone,True,building_id,building_name,sqlMysql) #添加用户在1小时外到访
    ackf_cookies = User_login.ackf_login_blue(ip_red,zcsachtkf)  #登录案场客服
    VisitAudit_id = Customer_visiting_record.getVisitAuditList(ip_red,ackf_cookies,customer_phone) # 查询案场客服审核用户时的ID
    Customer_visiting_record.VisitAudited(ip_red,ackf_cookies,VisitAudit_id)# 到访审核通过


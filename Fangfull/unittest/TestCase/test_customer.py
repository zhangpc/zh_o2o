# -*- coding:utf-8 -*-
#!/usr/bin/python
import unittest
from Fangfull.controller import User_login
from Fangfull.controller import Customer,Customer_visiting_record,Building,Company_employee
from config import Config


class Test_Customer(unittest.TestCase):
    def __init__(self,param,customer_phone,jg_broker_compary_phone,isdele_customer,zcsacjjy,zcsachtkf,zcsxmzj,building_name):
        self.param = param
        self.customer_phone = customer_phone
        self.jg_broker_compary_phone = jg_broker_compary_phone
        self.isdele_customer = isdele_customer
        self.zcsacjjy = zcsacjjy
        self.zcsachtkf = zcsachtkf
        self.building_name = building_name
        self.zcsxmzj = zcsxmzj
        # self.qm_broker_compary_phone = qm_broker_compary_phone

    #登录经纪人_添加客户_登录置业顾问添加客户到访_登录客服到访审核通过
    def test_brokerlogin_addcustomer_customerVisitingRecord_VisitAudited(self,param=None):

        # 机构经纪公司管理员账号 test13800000001
        # 机构经纪人账号: 13800000001
        # 全民经纪公司管理员账号 test13800000002
        # 全民经纪人账号: 13800000002
        # ['zcsxmzj','zcsacjjy','zcsacddlry','zcsachtkf','zcszbcw','zcsaccw','zcsjyshy']
        print("case:登录经纪人_添加客户_登录置业顾问添加客户到访_登录客服到访审核通过")
        if self.param == None:
            ip = Config.Ip()
            ip.set_Ipblue('http://test1www.xqshijie.com/')
            ip.set_Ipred('http://test2www.xqshijie.com/')
            ip_blue = ip.get_Ipblue()
            ip_red = ip.get_Ipred()
            sqlconnect = Config.SqlConnect()
            sqlMysql = sqlconnect.get_fangfull_test_sql()
        elif len(self.param)> 0 :
            ip_blue = self.param['ipblue']
            ip_red = self.param['ipred']
            sqlMysql = self.param['sqlMysql']

        zcsacjjy = self.zcsacjjy
        zcsachtkf = self.zcsachtkf
        customer_phone = self.customer_phone
        broker_compary_phone = self.jg_broker_compary_phone # 机构经纪人登录账号
        isdele_customer = self.isdele_customer
        customer_grade = '3'
        broker_cookies = User_login.broker_login(ip_blue,broker_compary_phone)  # 登录经纪人
        building_name = self.building_name #'新奇世界-半山半岛' '北京中弘大厦'# 新奇世界-长白水镇4号地 #'新奇世界-长白水镇5号地'
        building_id = Building.sql_getbuliding_id(building_name,sqlMysql)
        customer_id = Customer.add_customer(ip_blue,broker_cookies,customer_phone,building_id,building_name,customer_grade,isdele_customer,sqlMysql)  #给经纪人添加并报备用户,返回用户ID
        acjjy_cookies = User_login.acgly_login_red(ip_red,zcsacjjy) # 登录案场讲解员账号

        Customer_visiting_record.customerVisitingRecord(ip_blue,acjjy_cookies,customer_id,customer_phone,False,building_id,building_name,sqlMysql) #添加用户在1小时外到访到访
        ackf_cookies = User_login.ackf_login_blue(ip_red,zcsachtkf)  #登录案场客服
        VisitAudit_id = Customer_visiting_record.getVisitAuditList(ip_red,ackf_cookies,customer_phone) # 查询案场客服审核用户时的ID
        Customer_visiting_record.VisitAudited(ip_red,ackf_cookies,VisitAudit_id)# 到访审核通过

    #登录经纪人_添加客户_登录置业顾问添加客户在1小内到访，客户归中弘

    def test_brokerlogin_addcustomer_xmzj(self,param=None,customer_phone=None):
        print("case:登录经纪人_添加客户_登录置业顾问添加客户在1小内到访，客户归中弘")
        if self.param == None:
            ip = Config.Ip()
            ip.set_Ipblue('http://test1www.xqshijie.com/')
            ip.set_Ipred('http://test2www.xqshijie.com/')
            ip_blue = ip.get_Ipblue()
            ip_red = ip.get_Ipred()
            sqlconnect = Config.SqlConnect()
            sqlMysql = sqlconnect.get_fangfull_test_sql()
        elif len(self.param)> 0 :
            ip_blue = self.param['ipblue']
            ip_red = self.param['ipred']
            sqlMysql = self.param['sqlMysql']
        # ip_blue = param['ipblue']
        # ip_red = param['ipred']
        # sqlMysql = param['sqlMysql']
        zcsacjjy = self.zcsacjjy
        zcsachtkf = self.zcsachtkf
        zcsxmzj = self.zcsxmzj
        customer_phone = self.customer_phone
        broker_compary_phone = self.jg_broker_compary_phone # 机构经纪人登录账号
        isdele_customer = self.isdele_customer
        customer_grade = '3' #客户意向等级
        # for i in range (len(customer_phone)):
        broker_cookies = User_login.broker_login(ip_blue,broker_compary_phone)  # 登录经纪人
        building_name = self.building_name #'新奇世界-半山半岛' '北京中弘大厦'# 新奇世界-长白水镇4号地 #'新奇世界-长白水镇5号地'
        building_id = Building.sql_getbuliding_id(building_name,sqlMysql)
        customer_id = Customer.add_customer(ip_blue,broker_cookies,customer_phone,building_id,building_name,customer_grade,isdele_customer,sqlMysql)  #给经纪人添加并报备用户,返回用户ID

        acjjy_cookies = User_login.acgly_login_red(ip_red,zcsacjjy) # 登录案场讲解员账号
        Customer_visiting_record.customerVisitingRecord(ip_blue,acjjy_cookies,customer_id,customer_phone,True,building_id,building_name,sqlMysql) #添加用户在1小时内到访到访

        ackf_cookies = User_login.ackf_login_blue(ip_red,zcsachtkf)  #登录案场客服
        VisitAudit_id = Customer_visiting_record.getVisitAuditList(ip_red,ackf_cookies,customer_phone) # 查询案场客服审核用户时的ID
        Customer_visiting_record.VisitAudited(ip_red,ackf_cookies,VisitAudit_id)# 到访审核通过

        xmzj_cookies = User_login.xmzj_login_blue(ip_red,zcsxmzj)
        employee_id,employee_name = Company_employee.sql_Employee_UserMessage(zcsacjjy,sqlMysql)
        # Customer_visiting_record.post_submitDistribute(ip_red,xmzj_cookies,customer_id,employee_id,building_id,building_name,customer_grade)

        pass
    ## 经纪公司报备客户后进行预约
    def test_brokerlogin_addcustomer_customerAppointment(self,param=None):
        print("case:经纪公司报备客户后进行预约")
        if self.param == None:
            ip = Config.Ip()
            ip.set_Ipblue('http://test1www.xqshijie.com/')
            ip.set_Ipred('http://test2www.xqshijie.com/')
            ip_blue = ip.get_Ipblue()
            ip_red = ip.get_Ipred()
            sqlconnect = Config.SqlConnect()
            sqlMysql = sqlconnect.get_fangfull_test_sql()
        elif len(self.param)> 0 :
            print('走的param == 不为空')
            ip_blue = self.param['ipblue']
            ip_red = self.param['ipred']
            sqlMysql = self.param['sqlMysql']
        customer_phone = self.customer_phone
        broker_compary_phone = self.jg_broker_compary_phone # 机构经纪人登录账号
        isdele_customer = self.isdele_customer #是否删除已存在的客户
        broker_cookies = User_login.broker_login(ip_blue,broker_compary_phone)  # 登录经纪人
        building_name = self.building_name #'新奇世界-半山半岛' '北京中弘大厦'# 新奇世界-长白水镇4号地 #'新奇世界-长白水镇5号地'
        customer_grade = '3'#客户意向等级
        building_id = Building.sql_getbuliding_id(building_name,sqlMysql)
        customer_id = Customer.add_customer(ip_blue,broker_cookies,customer_phone,building_id,building_name,customer_grade,isdele_customer,sqlMysql)
        Customer_visiting_record.customerAppointment_savebroker(ip_blue,broker_cookies,customer_id,customer_phone,building_id) # 添加客户预约
        pass
    #经纪公司报备客户_添加预约_案场讲解员确认如期履约
    def test_customer_appointment(self,param=None):
        print("case:经纪公司报备客户_添加预约_案场讲解员确认如期履约")
        if self.param == None:
            ip = Config.Ip()
            ip.set_Ipblue('http://test1www.xqshijie.com/')
            ip.set_Ipred('http://test2www.xqshijie.com/')
            ip_blue = ip.get_Ipblue()
            ip_red = ip.get_Ipred()
            sqlconnect = Config.SqlConnect()
            sqlMysql = sqlconnect.get_fangfull_test_sql()
        elif len(self.param)> 0 :

            ip_blue = self.param['ipblue']
            ip_red = self.param['ipred']
            sqlMysql = self.param['sqlMysql']
        customer_phone = self.customer_phone
        broker_compary_phone = self.jg_broker_compary_phone # 机构经纪人登录账号
        isdele_customer = self.isdele_customer #是否删除已存在的客户
        customer_grade = '3'
        broker_cookies = User_login.broker_login(ip_blue,broker_compary_phone)  # 登录经纪人
        building_name = self.building_name #'新奇世界-半山半岛' '北京中弘大厦'# 新奇世界-长白水镇4号地 #'新奇世界-长白水镇5号地'
        building_id = Building.sql_getbuliding_id(building_name,sqlMysql)
        customer_id = Customer.add_customer(ip_blue,broker_cookies,customer_phone,building_id,building_name,customer_grade,isdele_customer,sqlMysql) # 添加客户报备
        Customer_visiting_record.customerAppointment_savebroker(ip_blue,broker_cookies,customer_id,customer_phone,building_id) # 添加客户预约
        appointment_status = '1'  ####'状态 1 预约 2确认 3如期履约 4爽约 5取消',
        appointmentid = Customer_visiting_record.get_myReserveList(ip_blue,broker_cookies,building_id,customer_id,customer_phone,appointment_status,sqlMysql)
        acjjy_cookies = User_login.acgly_login_blue(ip_red,'zcsacjjy') # 登录案场讲解员（置业顾问）
        Customer_visiting_record.appointment_status_set(ip_red,acjjy_cookies,appointmentid,'3') #讲解员确认预约，预约状态改变为“3如期履约”
        Customer_visiting_record.get_myReserveList(ip_blue,broker_cookies,building_id,customer_id,customer_phone,'3',sqlMysql) #经纪人查看预约状态是否正确






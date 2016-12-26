# -*- coding:utf-8 -*-
#!/usr/bin/python
import unittest
from Fangfull.controller import Broker,User_login,Broker_company
from config import Config

class Test_Pre_condition(unittest.TestCase):
    def __init__(self,param,jg_broker_compary_phone,qm_broker_compary_phone,nb_broker_compary_phone):
        self.param = param
        self.jg_broker_compary_phone = jg_broker_compary_phone
        self.qm_broker_compary_phone = qm_broker_compary_phone
        self.nb_broker_compary_phone = nb_broker_compary_phone

    def setUp(self):
        pass
    def tearDown(self):
        pass

    #创建机构经纪公司、管理员账号、经纪人账号
    def test_method_Creat_BrokercomparyAndBroker_jigou(self,param=None):
        print('case: 创建机构经纪公司、管理员账号、经纪人账号')
        print('当前连接信息：',self.param)
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

        broker_compary_phone = self.jg_broker_compary_phone#'13800000001'
        broker_compary_name = 'z机构经纪公司'+str(broker_compary_phone)
        admin_cookies = User_login.admin_login_red(ip_red)
        # company_property'公司类别 1机构经纪公司 2全民经纪公司 3|内部经纪公司' 4|渠道经纪公司,
        company_property = '1'

        Broker.sql_del_broker_msg(broker_compary_phone,sqlMysql)
        broker_compary_id = Broker.creat_Broker_company(ip_blue,admin_cookies,broker_compary_name,broker_compary_phone,company_property) # 创建经纪公司

        broker_companyadmin_name = Broker.savebrokerCompanyAdmin(ip_blue,admin_cookies,broker_compary_id,broker_compary_phone) #创建经纪公司管理员
        brokerCompany_cookies = User_login.broker_companylogin(ip_blue,broker_companyadmin_name)#经纪公司管理员登陆
        Broker_company.Broker_mysave(ip_blue,brokerCompany_cookies,broker_compary_phone) #创建经纪人

        print('机构经纪公司名称',broker_compary_name)
        print('机构经纪公司管理员账号',broker_companyadmin_name)
        print('机构经纪人账号:',broker_compary_phone)


    #创建全民经纪公司、管理员账号、经纪人登录账号
    def test_method_Creat_BrokercomparyAndBroker_quanming(self,param=None):
        print('case: 创建全民经纪公司、管理员账号、经纪人登录账号')
        print('当前连接信息：',self.param)
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


        broker_compary_phone = self.qm_broker_compary_phone#'13800000018'
        broker_compary_name = 'z全民经纪公司'+str(broker_compary_phone)
        admin_cookies = User_login.admin_login_red(ip_red)
        #company_property'公司类别 1机构经纪公司 2全民经纪公司 3|内部经纪公司' 4|渠道经纪公司,
        company_property = '2'
        Broker.sql_del_broker_msg(broker_compary_phone,sqlMysql)
        broker_compary_id = Broker.creat_Broker_company(ip_blue,admin_cookies,broker_compary_name,broker_compary_phone,company_property) # 创建经纪公司
        broker_companyadmin_name = Broker.savebrokerCompanyAdmin(ip_blue,admin_cookies,broker_compary_id,broker_compary_phone) #创建经纪公司管理员
        brokerCompany_cookies = User_login.broker_companylogin(ip_blue,broker_companyadmin_name)#经纪公司管理员登陆
        Broker_company.Broker_mysave(ip_blue,brokerCompany_cookies,broker_compary_phone) #创建经纪人
        print('全民经纪公司名称',broker_compary_name)
        print('全民经纪公司管理员账号',broker_companyadmin_name)
        print('全民经纪人账号:',broker_compary_phone)


    #创建内部经纪公司、管理员账号、经纪人登录账号
    def test_method_Creat_BrokercomparyAndBroker_neibu(self,param=None):
        print('case: 创建内部经纪公司、管理员账号、经纪人登录账号')
        print('当前连接信息：',self.param)
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


        broker_compary_phone = self.nb_broker_compary_phone
        broker_compary_name = 'z内部经纪公司'+str(broker_compary_phone)
        admin_cookies = User_login.admin_login_red(ip_red)
        #company_property'公司类别 1机构经纪公司 2全民经纪公司 3|内部经纪公司' 4|渠道经纪公司,
        company_property = '3'
        Broker.sql_del_broker_msg(broker_compary_phone,sqlMysql)
        broker_compary_id = Broker.creat_Broker_company(ip_blue,admin_cookies,broker_compary_name,broker_compary_phone,company_property) # 创建经纪公司
        broker_companyadmin_name = Broker.savebrokerCompanyAdmin(ip_blue,admin_cookies,broker_compary_id,broker_compary_phone) #创建经纪公司管理员
        brokerCompany_cookies = User_login.broker_companylogin(ip_blue,broker_companyadmin_name)#经纪公司管理员登陆
        Broker_company.Broker_mysave(ip_blue,brokerCompany_cookies,broker_compary_phone) #创建经纪人
        print('内部经纪公司名称',broker_compary_name)
        print('内部经纪公司管理员账号',broker_companyadmin_name)
        print('内部经纪人账号:',broker_compary_phone)






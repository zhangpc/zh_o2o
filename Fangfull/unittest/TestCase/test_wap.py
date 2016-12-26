# -*- coding:utf-8 -*-
#!/usr/bin/python
import unittest
from Fangfull.controller import User_login,Broker_company,Broker
from QuanminJingjiren.controller import Login
from config import Config

class Test_Wap(unittest.TestCase):
    def __init__(self,param,url_wap,jg_broker_compary_phone,qm_broker_compary_phone):
        self.param = param
        self.jg_broker_compary_phone = jg_broker_compary_phone
        self.qm_broker_compary_phone = qm_broker_compary_phone
        self.url_wap = url_wap

    def setUp(self):
        pass
    def tearDown(self):
        pass

    #机构经纪人：前端自动化登录 wap 全民经纪人添加身份证银行卡信息_进入房否后台登录admin账户_身份证银行卡审核通过
    def test_jigoujingjinren_creat_review(self,param=None):
        print('case：机构经纪人：前端自动化登录 wap 全民经纪人添加身份证银行卡信息_进入房否后台登录admin账户_身份证银行卡审核通过')
        print('当前连接信息：',self.param)
        # 机构经纪公司管理员账号 test13800000001
        # 机构经纪人账号: 13800000001
        # 全民经纪公司管理员账号 test13800000002
        # 全民经纪人账号: 13800000002
        # ['zcsxmzj','zcsacjjy','zcsacddlry','zcsachtkf','zcszbcw','zcsaccw','zcsjyshy']
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

        broker_companyadmin_phone = self.jg_broker_compary_phone
        Login.jigoujingjinren(self.url_wap,broker_companyadmin_phone,'自动化机构经纪人') # 進入前端自動化
        admin_cookies = User_login.admin_login_blue(ip_red)
        card_id,bank_id = Broker_company.get_BrokerList(ip_red,admin_cookies,broker_companyadmin_phone,1) # 返回身份证审核列表ID 和 银行卡审核列表ID
        Broker_company.reviewIdCard(ip_red,admin_cookies,card_id)# 身份证审核通过
        Broker_company.reviewBankCard(ip_red,admin_cookies,bank_id)# 银行卡审核通过

    #全民经纪人：前端自动化登录 wap 全民经纪人添加身份证银行卡信息_进入房否后台登录admin账户_身份证银行卡审核通过
    def test_quangmingjinjiren_creat_review(self,param=None):
        print('case：全民经纪人：前端自动化登录 wap 全民经纪人添加身份证银行卡信息_进入房否后台登录admin账户_身份证银行卡审核通过')
        print('当前连接信息：',self.param)
        # 机构经纪公司管理员账号 test13800000001
        # 机构经纪人账号: 13800000001
        # 全民经纪公司管理员账号 test13800000002
        # 全民经纪人账号: 13800000002
        # ['zcsxmzj','zcsacjjy','zcsacddlry','zcsachtkf','zcszbcw','zcsaccw','zcsjyshy']
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

        broker_companyadmin_phone = self.qm_broker_compary_phone#'13810000005'
        print('经纪人账号:',broker_companyadmin_phone)
        Login.quangminjinjiren(self.url_wap,broker_companyadmin_phone,'自动化全民经纪人')# 進入前端自動化
        admin_cookies = User_login.admin_login_blue(ip_red)
        card_id,bank_id = Broker_company.get_BrokerList(ip_red,admin_cookies,broker_companyadmin_phone,2) # 返回身份证审核列表ID 和 银行卡审核列表ID

        Broker_company.reviewIdCard(ip_red,admin_cookies,card_id)# 身份证审核通过
        Broker_company.reviewBankCard(ip_red,admin_cookies,bank_id)# 银行卡审核通过



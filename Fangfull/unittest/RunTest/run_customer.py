# -*- coding:utf-8 -*-
#!/usr/bin/python
import unittest
from config import Config
from Fangfull.unittest.TestCase.test_customer import Test_Customer

if __name__ == '__main__':

    sqlconnect = Config.SqlConnect()
    sqlMysql = sqlconnect.get_fangfull_beta_sql()
    basics_mssage = {
        'ipblue':'http://betawww.fangfull.com/',
        'ipred':'http://betaerp.fangfull.com/',
        'sqlMysql':sqlMysql,
        }

    # sqlconnect = Config.SqlConnect()
    # sqlMysql = sqlconnect.get_fangfull_test_sql()
    # basics_mssage = {
    #     'ipblue':'http://test1www.xqshijie.com/',
    #    'ipred':'http://test2www.xqshijie.com/',
    #     'sqlMysql':sqlMysql,
    #     }


    zcsacjjy = 'zcsacjjy' ##讲解员职业顾问
    zcsachtkf = 'zcsachtkf' ## 案场后台客服
    zcsxmzj = 'zcsxmzj' #项目总监
    jg_broker_compary_phone = '13700000130' #机构公司/经纪人登陆账号
    building_name = '新奇世界-半岛蓝湾' #'新奇世界-半山半岛' '北京中弘大厦'# 新奇世界-长白水镇4号地 #'新奇世界-长白水镇5号地' #新奇世界-济南鹊山 #济南中弘广场 #北京御马坊楼盘
    isdele_customer = True  #是否变更已存在的手机号
    customer_phone = '13000001238'
    # 13000001130
    testcustomer = Test_Customer(basics_mssage,customer_phone,jg_broker_compary_phone,isdele_customer,zcsacjjy,zcsachtkf,zcsxmzj,building_name)
    suite = unittest.TestSuite()
    # #登录经纪人_添加客户_登录置业顾问添加客户到访_登录客服到访审核通过
    suite.addTest(testcustomer.test_brokerlogin_addcustomer_customerVisitingRecord_VisitAudited)
    # #登录经纪人_添加客户_登录置业顾问添加客户在1小内到访，客户归中弘
    # suite.addTest(testcustomer.test_brokerlogin_addcustomer_xmzj)
    # # #经纪公司报备客户后进行预约
    # suite.addTest(testcustomer.test_brokerlogin_addcustomer_customerAppointment)
    # # #经纪公司报备客户_添加预约_案场讲解员确认如期履约
    # suite.addTest(testcustomer.test_customer_appointment)
    unittest.TextTestRunner(verbosity=2).run(suite)



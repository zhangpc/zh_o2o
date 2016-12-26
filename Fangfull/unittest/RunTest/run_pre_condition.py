# -*- coding:utf-8 -*-
#!/usr/bin/python
import unittest
from config import Config
from Fangfull.unittest.TestCase.test_pre_condition import Test_Pre_condition

if __name__ == '__main__':
    suite = unittest.TestSuite()


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
    #      'ipblue':'http://test1www.xqshijie.com/',
    #      'ipred':'http://test2www.xqshijie.com/',
    #      'sqlMysql':sqlMysql,
    # }

    jg_broker_compary_phone = '13700000130' #机构公司/经纪人登陆账号
    qm_broker_compary_phone = '13700000202' #全民经纪公司/经纪人登录账号
    nb_broker_compary_phone = '13700000302' #创建内部经纪公司、管理员账号、经纪人登录账号

    testpre_condition = Test_Pre_condition(basics_mssage,jg_broker_compary_phone,qm_broker_compary_phone,nb_broker_compary_phone)
    #创建机构经纪公司、管理员账号、经纪人账号
    suite.addTest(testpre_condition.test_method_Creat_BrokercomparyAndBroker_jigou)
    # # #创建全民经纪公司、管理员账号、经纪人登录账号
    # suite.addTest(testpre_condition.test_method_Creat_BrokercomparyAndBroker_quanming)
    # # # #创建内部经纪公司、管理员账号、经纪人登录账号
    # suite.addTest(testpre_condition.test_method_Creat_BrokercomparyAndBroker_neibu)
    unittest.TextTestRunner(verbosity=2).run(suite)
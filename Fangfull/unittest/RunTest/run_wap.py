# -*- coding:utf-8 -*-
#!/usr/bin/python
import unittest
from config import Config
from Fangfull.unittest.TestCase.test_wap import Test_Wap

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
    #      'ipblue':'http://test1www.xqshijie.com/',
    #      'ipred':'http://test2www.xqshijie.com/',
    #      'sqlMysql':sqlMysql,
    # }
    url_wap = 'http://testxqsj2.xqshijie.com/'
    # url_wap = 'https://betaqmjjr.xqshijie.com/'
    # url_beta = 'https://betaqmjjr.xqshijie.com/'
    
    jg_broker_compary_phone = '13700000121' #机构公司/经纪人登陆账号
    qm_broker_compary_phone = '13700000202' #全民经纪公司/经纪人登录账号

    suite = unittest.TestSuite()
    test_wap= Test_Wap(basics_mssage,url_wap,jg_broker_compary_phone,qm_broker_compary_phone)
    #机构经纪人：前端自动化登录 wap 全民经纪人添加身份证银行卡信息_进入房否后台登录admin账户_身份证银行卡审核通过
    # suite.addTest(test_wap.test_jigoujingjinren_creat_review)
    #全民经纪人：前端自动化登录 wap 全民经纪人添加身份证银行卡信息_进入房否后台登录admin账户_身份证银行卡审核通过
    suite.addTest(test_wap.test_quangmingjinjiren_creat_review)
    unittest.TextTestRunner(verbosity=2).run(suite)

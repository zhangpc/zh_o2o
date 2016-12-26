# -*- coding:utf-8 -*-
#!/usr/bin/python
from Fangfull.mondel import m_customer,m_broker_and_company,m_login,m_building
from Fangfull.controller import Customer,Building,User_login
from config import Config

class m_init():
    def __init__(self):
        self.m_customer = m_customer.m_Customer()
        self.m_broker_and_company = m_broker_and_company.m_Broker_And_Conpany()
        self.m_login = m_login.m_Login()
        self.m_bulidiing = m_building.m_Building()
    def getm_customer(self):
        return self.m_customer
if __name__ == '__main__':
    init = m_init()




    ip = Config.Ip()
    ip.set_Ipblue('http://test1www.xqshijie.com/')
    ip.set_Ipred('http://test2www.xqshijie.com/')
    ip_blue = ip.get_Ipblue()
    ip_red = ip.get_Ipred()
    sqlconnect = Config.SqlConnect()
    sqlMysql = sqlconnect.get_fangfull_test_sql()



    init.m_customer.set_customercellphone('13700000032')
    init.m_bulidiing.set_building_name('北京中弘大厦')













    zcsxmzj = 'zcsxmzj'
    zcsacjjy = 'zcsacjjy'
    zcsachtkf = 'zcsachtkf'

    jigoujinjiren = '13700000100' #机构经纪人账号 密码都是123456

    init.m_bulidiing.set_buliding_id(
        Building.sql_getbuliding_id(
            init.m_bulidiing.get_building_name(),sqlMysql
        )
    )
    broker_cookies = User_login.broker_login(ip_blue,jigoujinjiren)  # 机构登录经纪人

    customer_id = Customer.add_customer(ip_blue,
                                        broker_cookies,
                                        init.m_customer.get_customercellphone(),
                                        init.m_bulidiing.get_buliding_id(),
                                        init.m_bulidiing.get_building_name(),
                                        True,
                                        sqlMysql)  #给经纪人添加并报备用户,返回用户ID








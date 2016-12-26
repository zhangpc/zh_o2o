from Fangfull.controller import Building,User_login
from config import Config
import  xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.dom import Node
if __name__ == '__main__':
    dom = xml.dom.minidom.parse('request_xml.xml')

    tree = dom.documentElement
    root = tree.getroot()



    root = dom.fromstring(country_data_as_string)


    # print(root.getAttribute("type"))
    # aa = root.getElementsByTagName("login_broker")[0]
    # described = aa.getElementsByTagName("described")
    # print(described)
    # print(described[0].childNodes[0].nodeValue)



    # ip = Config.Ip()
    # ip.set_Ipblue('http://test1www.xqshijie.com/')
    # ip.set_Ipred('http://test2www.xqshijie.com/')
    # ip_blue = ip.get_Ipblue()
    # ip_red = ip.get_Ipred()
    #
    # jigoujinjiren = '13700000100' #机构经纪人账号 密码都是123456
    #
    # broker_cookies = User_login.broker_login(ip_blue,jigoujinjiren)  # 机构登录经纪人
    # print(broker_cookies)
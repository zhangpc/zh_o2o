# -*- coding:utf-8 -*-
#!/usr/bin/python
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

import tools_request
from Fangfull.controller import User_login
from config import Config
import bs4
import re

### 创建经纪人
def Broker_mysave(ipblue,cookis,broker_cellphone):

    url_broker_token = str(ipblue)+'broker/mycreate'
    content_token = tools_request.request_get(url_broker_token,None,cookies=cookis)
    soup = bs4.BeautifulSoup(content_token,'html.parser')
    get_input_all = soup.find_all('input')
    # print(get_input_all)
    broker_token = re.findall('<input name="mysavebroker_token" type="hidden" value="(\w+)"/>',str(get_input_all))[0]
    # print(broker_token)
    url = str(ipblue)+'Broker/mysave'

    # print('经纪人手机号',broker_cellphone)
    params = {
        'Brokerage[ids]':'0',
        'Brokerage[ids]':'0',
        'mysavebroker_token':str(broker_token),
        'Broker[broker_email]':'ztx1501@sina.com',
        'Broker[broker_cellphone]':str(broker_cellphone),
        'Broker[broker_name]':'自经纪人'+str(broker_cellphone),
        'Broker[identity_card]':'65400000000000000',
        'Broker[broker_province]':'1',
        'Broker[broker_city]':'1001',
        'Broker[broker_county]':'1001001',
        'Broker[broker_picture]':'',
        'Broker[birthday]	':'',
        'Broker[username]	':str(broker_cellphone),
        'Broker[password]	':'123456',
        'Broker[status]':'1',
        'yt0':'保 存',
    }
    tools_request.post_Request(url,params,cookies=cookis)


#查询机构经纪人审核列表,通过经纪人ID，返回身份证审核列表ID 和 银行卡审核列表ID
def get_BrokerList(ipred,cookies,phone,company_property):
    if company_property == 1: # 机构经纪人
        list = 'agentBrokerList'
        r_url =  "r=product/agentBrokerAdmin/"
        # url = Config_IP.IP_red + "admin.php?r=product/agentBrokerAdmin/agentBrokerList&group[name]=&group[phone]="+str(phone)+"&group[company]=&group[idNumb]=&group[start_time]=&group[status]=&group[id_status]=&group[card_status]=&group[submit_type]='yt0'"
    elif company_property == 2:#全民经纪人
        list = 'qmBrokerList'
        r_url = 'r=product/qmBrokerAdmin/'
        # r_url = Config_IP.IP_red + "admin.php?r=product/qmBrokerAdmin/qmBrokerList&group[name]=&group[phone]="+str(phone)+"&group[company]=&group[idNumb]=&group[start_time]=&group[status]=&group[id_status]=&group[card_status]=&group[submit_type]='yt0'"

    url = str(ipred) + "admin.php?"+ r_url+ list +"&group[name]=&group[phone]="+str(phone)+"&group[company]=&group[idNumb]=&group[start_time]=&group[status]=&group[id_status]=&group[card_status]=&group[submit_type]='yt0'"
    content = tools_request.request_get(url,None,cookies=cookies)

    # print(content)
    soup = bs4.BeautifulSoup(content,'html.parser')
    get_table_all = soup.find_all('table')

    print('----------------------------------')
    # print(get_table_all)
    # <a href="admin.php?r=product/agentBrokerAdmin/view&methed=1&id=708072" class="btn btn-xs btn-info">
    #broker_id = re.findall('<a class="btn btn-xs btn-success" href="admin.php\?r=product/agentBrokerAdmin/view&amp;methed=2&amp;id=(\w+)">',str(get_table_all))[0]

                           # '<a class="btn btn-xs btn-info" href="admin.php?          view&amp;methed=1&amp;id=712450">'
    broker_id = re.findall('<a class="btn btn-xs btn-success" href="admin.php\?' +str(r_url)+ 'view&amp;methed=2&amp;id=(\w+)">',str(get_table_all))[0]
    getreviewcard_Id,getbank_Id= getreviewcardId(ipred,cookies,broker_id,company_property)

    return getreviewcard_Id,getbank_Id

# 获取身份证和银行卡审核时传递的ID
def getreviewcardId(ipred,cookies,broker_id,company_property):
    if broker_id != None:
        if company_property == 1:
            url = str(ipred) + "admin.php?r=product/agentBrokerAdmin/view&methed=2&id="+str(broker_id)
        elif company_property == 2:
            url = str(ipred) + "admin.php?r=product/qmBrokerAdmin/view&methed=2&id="+str(broker_id)

        content = tools_request.request_get(url,None,cookies=cookies)
        soup = bs4.BeautifulSoup(content,'html.parser')
        get_input_all = soup.find_all('input')
        # print(get_input_all)
        getreviewcardId = re.findall('<input name="id\[id\]" type="hidden" value="(\w+)">',str(get_input_all))[0]
        getbankId = re.findall('<input name="bank\[card_id\]" type="hidden" value="(\w+)">',str(get_input_all))[0]
        # print(get_input_all)
        # print(getreviewcardId)
        # print(getbankId)
        return getreviewcardId,getbankId
    else:
        print('检查是否提交身份证和银行卡信息')
        return None,None


# 身份证银行卡审核
def reviewIdCard(ipred,cookies,card_id):

    url = str(ipred) + 'admin.php?r=product/qmBrokerAdmin/reviewIdCard'
    params = {
        'id[id]':str(card_id),
        'id[status]':'2',
        'id[comment]':'自动化身份证审核通过'+str(card_id),
    }
    tools_request.post_Request(url,params,cookies=cookies)

# 银行卡审核
def reviewBankCard(ipred,cookies,bank_Id):
    url = str(ipred) + 'admin.php?r=product/qmBrokerAdmin/reviewBankCard'
    params = {
        'bank[card_id]':str(bank_Id),
        'bank[status]':'2',
        'bank[comment]':'自动化银行卡审核通过',
    }
    tools_request.post_Request(url,params,cookies=cookies)


if __name__ =='__main__':

    ip = Config.Ip()
    ip.set_Ipblue('http://test1www.xqshijie.com/')
    ip.set_Ipred('http://test2www.xqshijie.com/')
    ip_blue = ip.get_Ipblue()
    ip_red = ip.get_Ipred()

    broker_compary_phone = '13690000000'
    admin_cookies = User_login.admin_login_blue(ip_red)
    card_id,bank_id = get_BrokerList(ip_red,admin_cookies,broker_compary_phone,1) # 返回身份证审核列表ID 和 银行卡审核列表ID

    reviewIdCard(ip_red,admin_cookies,card_id)# 身份证审核通过
    reviewBankCard(ip_red,admin_cookies,bank_id)# 银行卡审核通过

    # broker_compary_name = '自动化测试12'
    # broker_compary_phone = '13680001012'
    # admin_cookies = User_login.admin_login_red()
    # broker_compary_id = Broker.creat_Broker_company(admin_cookies,broker_compary_name,broker_compary_phone) # 创建经纪公司
    # broker_companyadmin_name = Broker.savebrokerCompanyAdmin(admin_cookies,broker_compary_id,broker_compary_phone) #创建经纪公司管理员
    # brokerCompany_cookies = User_login.broker_companylogin(broker_companyadmin_name)#经纪公司管理员登陆
    # Broker_company.Broker_mysave(brokerCompany_cookies,broker_compary_phone) #创建经纪人
    # print('经纪公司管理员账号',broker_companyadmin_name)
    # print('经纪人账号:',broker_compary_phone)

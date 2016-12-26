# -*- coding:utf-8 -*-
#!/usr/bin/python
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

import tools_request
from Fangfull.controller import User_login,Broker_company,Customer,Customer_visiting_record
from Fangfull.controller import User_login,Broker_company
import tools_mysql
from config import Config
import bs4
import re,time
# sql_connect = Config.sql_connect(Config.sql_index).set_connect()

### 创建经纪公司
def creat_Broker_company(ipblue,cookies,broker_compary_name,broker_compary_phone,company_property):
    creatBrokercompany_url = str(ipblue)+"manager/createbrokerCompany"

    savebrokercompany_token_text = tools_request.request_get(creatBrokercompany_url,None,cookies=cookies)
    re_input_token = re.findall(r'<input type="hidden" name="savebrokercompany_token" value="(\w+)" />',savebrokercompany_token_text)
    signature_date = time.strftime("%Y-%m-%d",time.localtime())
    start_time = time.strftime("%Y-%m-%d",time.localtime())
    # print(start_time)
    # print(re_input_token[0])
    parameter={
        'savebrokercompany_token':re_input_token[0],
        'BrokerCompany[ids]':'0',
        'BrokerCompany[name]':str(broker_compary_name),
        'BrokerCompany[company_property]':str(company_property),#'公司类别 1机构经纪公司 2全民经纪公司 3|内部经纪公司' 4|渠道经纪公司,
        'BrokerCompany[phone]':'010-88888888',
        'BrokerCompany[company_province]':'1',# 省
        'BrokerCompany[company_city]':'1001',#市
        'BrokerCompany[company_county]':'1001002',#区
        'BrokerCompany[company_address]':'地址：自动化测试添加',
        'BrokerCompany[fax]':'010-88888888',
        'BrokerCompany[contact_person]':'联系人',
        'BrokerCompany[contact_phone]':str(broker_compary_phone),
        'BrokerCompany[logo]':'/upload/20161216/201612161028581481855338.png',
        'BrokerCompany[license_url]':'/upload/20161216/201612161028581481855338.png',
        'contract_num':'',
        'signature_date':str(signature_date),
        'start_time':str(start_time),
        'end_time':'',
        'contract_id':'',
        'BrokerCompany[description]':'公司简介:'+str(broker_compary_name),
        'BrokerCompany[status]':'1',
    }
    url = str(ipblue)+'manager/saveBrokerCompany'
    Content = tools_request.post_Request(url,parameter,cookies=cookies)
    # print(Content)
    broker_compary_id = get_brokercompany(ipblue,cookies,broker_compary_name)
    # print(broker_compary_id)
    return broker_compary_id

## 查询经纪公司，并删除已存在的经纪公司和经纪公司管理员
def sql_del_broker_msg(contact_phone,sql_connect):
    ## 查询经纪公司
    try:
        is_broker_company_id = tools_mysql.MysqlConnect('select company_id from broker_company where contact_phone = '+str(contact_phone),sql_connect)

    except:
        is_broker_company_id = None

    brokercompany_id = []

    if len(is_broker_company_id) > 0 :
        for i in range(len(is_broker_company_id)):
            if len(is_broker_company_id[i])> 0:
                for j in range(len(is_broker_company_id[i])):
                    brokercompany_id.append(is_broker_company_id[i][j])
    # print('经纪公司ID',is_broker_company_id)

    type_broker_id = []
    for i in range(len(brokercompany_id)):
        type_broker_id.append(tools_mysql.MysqlConnect('select broker_id from broker where company_id = '+str(brokercompany_id[i]),sql_connect))

    broker_id = []
    for i in range(len(type_broker_id)):
        if len(type_broker_id[i])>0:
            for j in range(len(type_broker_id[i])):
                if len(type_broker_id[i][j])>0:
                    for k in range(len(type_broker_id[i][j])):
                        # if type_broker_id[i][j][k]!= None:
                        broker_id.append(type_broker_id[i][j][k])

    # print('经纪人ID',broker_id)
    ## 修改经纪公司，给经纪公司名称和手机号做标示
    if len(brokercompany_id)> 0:
        for i in range(len(brokercompany_id)):
            sql_str = 'update broker_company bc set bc.name = '+'"'+ "删除自动化机构经纪公司测试"+'"' +' ,bc.contact_phone =' +'"'+"删除:" + str(contact_phone)+'"' + ' where bc.company_id ='+str(brokercompany_id[i])
            tools_mysql.MysqlConnect(sql_str,sql_connect)

    ## 查询经纪公司下是否有管理员，如果有就返回管理员ID
    is_broker_admin = []
    try:
        for i in range(len(brokercompany_id)):
            is_broker_admin.append(tools_mysql.MysqlConnect('select company_admin_id from broker_company_admin where company_id = ' + str(brokercompany_id[i]),sql_connect))
    except:
        is_broker_admin = None

    type_company_admin_id = []
    if len(is_broker_admin) > 0 :
        for i in range(len(is_broker_admin)):
            if len(is_broker_admin[i])> 0:
                for j in range(len(is_broker_admin[i])):
                    if is_broker_admin[i][j] != None:
                        type_company_admin_id.append(is_broker_admin[i][j])

    company_admin_id = []
    for i in range(len(type_company_admin_id)):
        for j in range(len(type_company_admin_id[i])):
            if type_company_admin_id[i][j]!=None:
                company_admin_id.append(type_company_admin_id[i][j])

    ## 修改经纪公司管理员，给管理员名称和手机号做标示
    if len(company_admin_id) > 0:
        for i in range(len(company_admin_id)):
            update_broker_company_admin = 'update broker_company_admin bca set bca.admin_name = ' + '"删除自动化机构经纪公司管理员'+'"' + ' where company_admin_id = '+str(company_admin_id[i])
            tools_mysql.MysqlConnect(update_broker_company_admin,sql_connect)


    ## 修改经纪人，将经纪人从经纪
    # print('经纪人ID',broker_id)

    type_broker_del = tools_mysql.MysqlConnect('select broker_id from broker where username = '+"'"+str(contact_phone)+"'"+' or broker_cellphone = '+"'"+str(contact_phone)+"'",sql_connect)
    broker_del = []
    if len(type_broker_del) > 0 :
        for i in range(len(type_broker_del)):
            if len(type_broker_del[i])>0:
                for j in range (len(type_broker_del[i])):
                    if type_broker_del[i][j]!=None:
                        broker_del.append(type_broker_del[i][j])
    # print(broker_del)

    for i in range(len(broker_del)):
        update_broker ='UPDATE broker b set b.broker_cellphone = '+'"'+ "自动化修改经纪人"+'"' +' ,b.broker_name = ' +'"'+"弃用"+ '"'+  ',b.username=' +'"'+"弃用"+'"' +' where b.broker_id ='+str(broker_del[i])
        tools_mysql.MysqlConnect(update_broker,sql_connect)

# 查询经纪公司名称
def get_brokercompany(ipblue,cookies,broker_compary_name):
    time.sleep(2)
    url = str(ipblue)+"manager/adminbrokercompany"
    params = {
    'area':'',
    'company_province':'',
    'company_city':'',
    'company_county':'',
    'level':'',
    'brokercompany_status':'-1',
    'BrokerCompany[company_property]':'',
    'BrokerCompany[name]':str(broker_compary_name),
    'BrokerCompany[phone]':'',
    'BrokerCompany[company_cellphone_status]':'',
    'yt0':'搜 索',
    }

    Content= tools_request.post_Request(url,params,cookies=cookies)
    soup = bs4.BeautifulSoup(Content,'html.parser')
    get_talbe_all = soup.find_all('table')

    broker_compary_id = re.findall('<td data-id="(\w+)" data-target="#selBrokerageitem_Modal" data-title="\w+" data-title_com="'+str(broker_compary_name)+'"',str(get_talbe_all))[0]
    # print(broker_compary_id)
    return broker_compary_id

###创建经纪公司管理员
def savebrokerCompanyAdmin(ipblue,cookies,broker_compary_id,broker_compary_phone):

    url_token = str(ipblue)+'/manager/createbrokerCompanyAdmin/bcid/'+str(broker_compary_id)+'/entrance/manageradmin'
    Conten_token = tools_request.request_get(url_token,None,cookies=cookies)
    soup = bs4.BeautifulSoup(Conten_token,'html.parser')
    get_input_all = soup.find_all('input')
    savebrokercompanyadmin_token = re.findall(r'<input name="savebrokercompanyadmin_token" type="hidden" value="(\w+)"',str(get_input_all))[0]
    # print(savebrokercompanyadmin_token)
    BrokerCompanyAdmin_name = 'test'+str(broker_compary_phone)
    params = {
    'savebrokercompanyadmin_token':str(savebrokercompanyadmin_token),
    'entrance':'manageradmin',
    'county':'',
    'city':'',
    'province':'',
    'area':'',
    'from':'',
    'status':'',
    'BrokerCompanyAdmin[ids]':'0',
    'BrokerCompanyAdmin[company_id]':broker_compary_id,
    'BrokerCompanyAdmin[admin_name]':BrokerCompanyAdmin_name,
    'BrokerCompanyAdmin[admin_passwd]':'123456',
    'BrokerCompanyAdmin[status]':'2',
    'yt0':'保 存',
    }

    url = str(ipblue) + 'manager/savebrokerCompanyAdmin'
    content = tools_request.post_Request(url,params,cookies=cookies)
    return BrokerCompanyAdmin_name


if __name__ =='__main__':
    ip = Config.Ip()
    ip.set_Ipblue('http://test1www.xqshijie.com/')
    ip.set_Ipred('http://test2www.xqshijie.com/')
    ip_blue = ip.get_Ipblue()
    ip_red = ip.get_Ipred()
    sqlconnect = Config.SqlConnect()
    sqlMysql = sqlconnect.get_fangfull_test_sql()

    zcsxmzj = 'zcsxmzj'
    zcsacjjy = 'zcsacjjy'
    zcsachtkf = 'zcsachtkf'
    broker_compary_name = '自动化测试1'
    broker_compary_admin_phone = '13680000000'
    admin_cookies = User_login.admin_login_red(ip_red)
    sql_del_broker_msg(broker_compary_admin_phone,sqlMysql)
    broker_compary_id = creat_Broker_company(ip_blue,admin_cookies,broker_compary_name,broker_compary_admin_phone,1)
    broker_companyadmin_name = savebrokerCompanyAdmin(ip_blue,admin_cookies,broker_compary_id,broker_compary_admin_phone)

    broker_compary_phone = '13690000000'
    brokerCompanyAdmin_cookies = User_login.broker_companylogin(ip_blue,broker_companyadmin_name)#经纪公司管理员登陆
    Broker_company.Broker_mysave(ip_blue,brokerCompanyAdmin_cookies,broker_compary_phone) ### 创建经纪人

    print('经纪公司管理员账号',broker_companyadmin_name)
    print('经纪人账号:',broker_compary_phone)




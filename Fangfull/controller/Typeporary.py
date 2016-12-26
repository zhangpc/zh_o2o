# -*- coding:utf-8 -*-
#!/usr/bin/python
import tools_request,tools_mysql
from config import Config
# sql_connect = Config.sql_connect(Config.sql_index).set_connect()
# 通过传递公司类型返回公司经纪人手机号
# 公司类型，经纪人状态，经纪公司状态，返回多少个手机号
def getsql_phone(company_property,broker_status,brokercompany_status,number,sql_connect):
    # company_property 1 机构经纪人
    # company_property 2 全民经纪人
    # company_property 3 内部经纪人
    # status 1 符合，其他不符合
    sql_broker_cellphone = tools_mysql.MysqlConnect("select b.broker_cellphone FROM broker b where b.status =" +str(broker_status)+" and b.company_id in(select company_id from broker_company bc where bc.status=" +str(brokercompany_status)+" and bc.company_property = "+ str(company_property)+") order by b.broker_id LIMIT "+str(number),sql_connect)

    broker_cellphone = []

    for i in range(len(sql_broker_cellphone)):
        if (len(sql_broker_cellphone[i])> 0 ):
            for j in range (len(sql_broker_cellphone[i])):
                broker_cellphone.append(sql_broker_cellphone[i][j])
        else:
            broker_cellphone.append(sql_broker_cellphone[i])

    return broker_cellphone,company_property,broker_status,brokercompany_status
def getIsBroker(ipred,broker_cellphone,company_property,broker_status,brokercompany_status):
    if len(broker_cellphone) == 0:
        print("没有符合条件的手机号")
        return

    for i in range(len(broker_cellphone)):
        sign = str(get_sin(broker_cellphone[i]))
        sign_temp = sign[2:]
        url = str(ipred) + "api.php?r=apixqsj/GetIsBroker&client=xqsj&app_key=0RINESDW&v=1.0&phone="+str(broker_cellphone[i])+"&sign="+str(sign_temp)
        re = tools_request.get_request(url)

        # if company_property == 1 or company_property == 2:
        if broker_status != 0 and brokercompany_status != 0:
            # print(re.json(),broker_cellphone[i])
            get_Assert(i,broker_cellphone[i],company_property,re.json()['data']['isbroker'],sign_temp)
        else:
            if broker_status != 0:
                print("经纪人状态不是启用")

            elif brokercompany_status !=0 :
                print("经纪公司状态不是启用")
                print(str(i)+" :" + str(broker_cellphone[i])+'   '+str(re.json()),"成功的机构经纪人",str(sign_temp))

            elif broker_status !=0 and brokercompany_status != 0:
                print("经纪公司和经纪人状态不是启用")

def get_Assert(num,broker_cellphone,company_property,Assert2,sign_temp):

    # for i in range(len(broker_cellphone)):
    if company_property == 1 :
        if tools_request.Assert('1',str(Assert2),0) == False:
            print(str(num)+" :" + str(broker_cellphone)+'   '+str(Assert2),"失败的机构经纪人",str(sign_temp))
        # else:
        #     print(str(broker_cellphone),"成功的机构经纪人")
    elif company_property == 2:
        if tools_request.Assert('0',str(Assert2),0) == False:
            print(str(num)+" :" + str(broker_cellphone)+'   '+str(Assert2),"失败的全民经纪人",str(sign_temp))
        # else:
        #     print(str(broker_cellphone),"成功的全民经纪人")
def get_sin(phone):
    url = 'http://192.168.9.159/t.php?phone='+phone
    sign = tools_request.get_request_cookies(url,None)
    return str(sign)
if __name__ == '__main__':
    #
    # sqlconnect = Config.SqlConnect()
    # sqlMysql = sqlconnect.get_fangfull_test_sql()
    # broker_cellphone,company_property,broker_status,brokercompany_status = getsql_phone(1,0,0,1000,sqlMysql)
    # getIsBroker(broker_cellphone,company_property,broker_status,brokercompany_status)

    import datetime
    starttime = datetime.datetime.now()
    #long running
    print('dddddddddddddddddddddd')
    endtime = datetime.datetime.now()
    print ((endtime - starttime).seconds)
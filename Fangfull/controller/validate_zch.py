# -*- coding:utf-8 -*-
#!/usr/bin/python
import tools_mysql
from config import Config
import requests,json
import base64,datetime,time
from time import ctime,sleep

from Fangfull.common import writexls,readxls
def gettoken():
    # print("登录用户")
    url_token = 'http://test.console.xqshijie.com/access_token.json?username=test1&password=1234'
    content = requests.get(str(url_token))
    # print("登录成功")
    return content

def getvalidate(token,customer_phone,strassert,xlsname,*args):
    # print(len(customer_phone),customer_phone)

    headers = 'access_token:'+token.json()['data']
    bese_encode = base64.b64encode(str(headers).encode('utf-8'))
    bese_str = 'Basic '+str(bese_encode,'utf-8')
    req_session = requests.session()


    maxlen = len(customer_phone)
    isassert = [1]*maxlen
    ismessage = [1]*maxlen
    isjson = [1]*maxlen
    ismicroseconds = [1]*maxlen
    iscode = [1]*maxlen
    istrue = [1]*maxlen
    isdata = [1]*maxlen

    print("开始查询比对实际值")
    print(maxlen,customer_phone)
    for i in range(len(customer_phone)):
        # 为防止登录过期，每次查询新数据都进行重新登录
        url_validate = "http://test.console.xqshijie.com/customer/validate/"+str(customer_phone[i])+".json"
        response = req_session.get(str(url_validate),headers = {'Authorization':bese_str})
        ismicroseconds[i] = str(response.elapsed.microseconds)
        isjson[i] = str(json.dumps(response.json(),ensure_ascii=False))
        istrue[i] = str(json.dumps(response.json()['error'],ensure_ascii=False))
        isdata[i] = str(json.dumps(response.json()['data'],ensure_ascii=False))
        iscode[i] = str(json.dumps(response.json()['code'],ensure_ascii=False))
        ismessage[i] = str(json.dumps(response.json()['message'],ensure_ascii=False))
        if  strassert in str(json.dumps(response.json()['code'],ensure_ascii=False)):
            isassert[i] = str("符合预期")
        else:
            isassert[i] = str("不符合预期值")
        if (len(args)>0):
            print(isjson[i],istrue[i],isdata[i],iscode[i],ismessage[i],isassert[i],args[0][i],customer_phone[i],' ',str(ismicroseconds[i])+"毫秒",' ',str(round((i+1)/maxlen,2)*100) + '%','  ',str(i+1)+'/'+str(maxlen))
        else:
            print(isjson[i],istrue[i],isdata[i],iscode[i],ismessage[i],isassert[i],customer_phone[i],' ',str(ismicroseconds[i])+"毫秒",' ',str(round((i+1)/maxlen,2)*100) + '%','  ',str(i+1)+'/'+str(maxlen))
    # rw = writexls.Writexls()
    # rw.add_sheet('test1')
    # if (len(args)>0):
    #     rw.xls_write_array(isjson,istrue,isdata,iscode,ismessage,isassert,args[0],customer_phone,ismicroseconds)
    # else:
    #     rw.xls_write_array(isjson,istrue,isdata,iscode,ismessage,isassert,customer_phone,ismicroseconds)
    # timenew = str(time.strftime('%Y-%m-%d_%H_%M_%S',time.localtime(time.time())))
    # rw.save_xls(str(xlsname)+str(timenew)+'.xls')

def sql_customer_cellphone(strsql):
    print("查询符合条件的用户手机号")
    sqlconnect = Config.SqlConnect()
    sqlMysql = sqlconnect.get_fangfull_test_sql()
    strsql = strsql
    typecellphone = tools_mysql.MysqlConnect(strsql,sqlMysql)
    cellphone = []
    for i in range(len(typecellphone)):
        for j in range(len(typecellphone[i])):
            cellphone.append(str(typecellphone[i][j]))
    print("查询房否后台已成交用户手机号完成，进行返回")
    return cellphone
def sql_customer_cellphone_complex(strsql):
    print("查询符合条件的用户手机号")
    sqlconnect = Config.SqlConnect()
    sqlMysql = sqlconnect.get_fangfull_test_sql()
    strsql = strsql
    typedata = tools_mysql.MysqlConnect(strsql,sqlMysql)
    cellphone = []
    customerid = []
    for i in range(len(typedata)):
        customerid.append(typedata[i][0])
        cellphone.append(typedata[i][1])

    print("查询房否后台已成交用户手机号完成，进行返回")
    return customerid,cellphone

# 读取excel
def get_readxls(xlsname):
    my_readxls = readxls.Readxls(xlsname)
    table = my_readxls.readsheet('test1')
    phone = my_readxls.cell_value_AppointNcols(table,6)
    return phone
if __name__ == '__main__':
    token = gettoken()
    # 200 是老用户  602 没有订单  601 无效手机号
    # '订单状态： 1已认购|2已取消|3已签约'
    # status = '3'
    # strsql = "select cu.customer_cellphone from customer cu where cu.customer_id in(select bka.coustomer_id from brokerage bka where bka.status = "+"'"+str(status)+"'"+") and cu.customer_cellphone != ''"
    # cellphone = sql_customer_cellphone(strsql)
    # getvalidate(token,cellphone,'200','房否后台_老用户')


    # print('========================================')
    # ##  已取消订单的用户不算老用户
    # strsql = "select cu.customer_cellphone from customer cu inner join ( SELECT bka.coustomer_id as coustomer_id FROM brokerage bka WHERE bka.STATUS = 1 or bka.STATUS = 2 and bka.coustomer_id not in ( select bkage.coustomer_id from brokerage bkage where bkage.STATUS = 3 ) ) ggg on cu.customer_id = ggg.coustomer_id"
    # cellphone = sql_customer_cellphone(strsql)
    # getvalidate(token,cellphone,'602','房否后台_已认购or已取消')


    ## 房否订单表中的新奇世界-成交客户
    # strsql = "select xqsj_phone from brokerage where xqsj_phone != '' and status = '3'"
    # cellphone = sql_customer_cellphone(strsql)
    # getvalidate(token,cellphone,'200','房否后台_新奇世界_老客户')

    ## 房否订单表中的新奇世界-非成交客户
    # strsql = "select xqsj_phone from brokerage where status != '3' and xqsj_phone != '' and coustomer_id not in (select br.coustomer_id from brokerage br where br.status = '3' and br.xqsj_phone != '')"
    # cellphone = sql_customer_cellphone(strsql)
    # getvalidate(token,cellphone,'602','房否后台_新奇世界_已认购or已取消')

    ## 房否后台没有订单记录的客户
    # strsql = "select ct.customer_id,ct.customer_cellphone from customer ct where ct.customer_cellphone !='' and ct.customer_id not in (select br.coustomer_id from brokerage br) order by ct.customer_id LIMIT 4000,4500"
    # customerid,cellphone = sql_customer_cellphone_complex(strsql)
    # getvalidate(token,cellphone,'602','房否后台_没有订单记录的用户前4k_4K5',customerid)

    # cellphone = ['13810021245']
    # getvalidate(token,cellphone,'200','新奇世界_13810021245非老用户')


    # strsql = "select ct.customer_id,ct.customer_cellphone from customer ct where ct.customer_cellphone !='' and ct.customer_id not in (select br.coustomer_id from brokerage br) order by ct.customer_id LIMIT 4000,4500"
    # customerid,cellphone = sql_customer_cellphone_complex(strsql)
    # cellphone = ['15553184446']
    # customerid = ['17827']
    # getvalidate(token,cellphone,'602','房否后台_没有订单记录的用户1个',customerid)













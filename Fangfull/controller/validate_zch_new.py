# -*- coding:utf-8 -*-
#!/usr/bin/python
import tools_mysql
from config import Config
import requests,json
import base64,datetime,time
from time import ctime,sleep
import threading
import traceback
from Fangfull.common import writexls,readxls

def gettoken():
    print("登录用户")
    url_token = 'http://test.console.xqshijie.com/access_token.json?username=test1&password=1234'
    try:
        content = requests.get(str(url_token))
        req_session,bese_str = getreqSession(content)
        print("登录成功")
        return req_session,bese_str
    except :
        print("登录失败",Exception.args)
        return None
    return None
def getreqSession(token):
    headers = 'access_token:'+token.json()['data']
    bese_encode = base64.b64encode(str(headers).encode('utf-8'))
    bese_str = 'Basic '+str(bese_encode,'utf-8')
    req_session = requests.session()
    print("返回session，bese")
    return req_session,bese_str

def sql_customer_cellphone(strsql,sqlconnect):
    print("查询符合条件的用户手机号")
    typedata = tools_mysql.MysqlConnect(strsql,sqlconnect)
    # sqlMysql = sqlconnect.get_fangfull_test_sql()
    # sqlMysql = sqlconnect.get_xqsj_test_sql()
    # strsql = strsql
    # typecellphone = tools_mysql.MysqlConnect(strsql,sqlMysql)
    cellphone = []
    for i in range(len(typedata)):
        for j in range(len(typedata[i])):
            cellphone.append(str(typedata[i][j]))
    print("查询房否后台已成交用户手机号完成，进行返回")
    return cellphone

def sql_customer_cellphone_complex(strsql,sqlconnect):
    print("查询符合条件的用户手机号")
    # strsql = strsql
    typedata = tools_mysql.MysqlConnect(strsql,sqlconnect)
    cellphone = []
    customerid = []
    # print(typedata)
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

def openxls():
    rwxls = writexls.Writexls()
    rwxls.add_sheet('test1')
    return rwxls
def rwxls(rw,number,istrue,isdata,iscode,ismessage,isassert,customer_phone,ismicroseconds,*args):
    if (len(args)>0):
        rw.xls_write_nrows(number,istrue,isdata,iscode,ismessage,isassert,args[0],customer_phone,ismicroseconds)
    else:
        rw.xls_write_nrows(number,istrue,isdata,iscode,ismessage,isassert,customer_phone,ismicroseconds)

def savexls(rw,xlsname):
    print("进入xls保存流程")
    timenew = str(time.strftime('%Y-%m-%d_%H_%M_%S',time.localtime(time.time())))
    rw.save_xls(str(xlsname)+str(timenew)+'.xls')

# 读取excel
def get_readxls(xlsname,sheelname,cols):
    my_readxls = readxls.Readxls(xlsname)
    table = my_readxls.readsheet(sheelname)
    phone = my_readxls.cell_value_AppointNcols(table,cols)
    return phone

CONSTANT = 1
class RequestThread(threading.Thread):
    # 构造函数
    def __init__(self,req_session,bese_str,customer_phone,strassert,getxls,number,numberMax,xlsname,*args):
        threading.Thread.__init__(self)
        self.test_count = 0
        self.req_session = req_session
        self.bese_str = bese_str
        self.customer_phone = customer_phone
        self.strassert = strassert
        self.isassert = ''
        self.getxls = getxls
        self.number = number
        self.xlsname = xlsname
        self.numberMax = numberMax
        self.numberone = 0
        self.args = args
    def run(self):
        self.getvalidate()
    def getlenEnumerate(self):
        return len(threading.enumerate())
    def getvalidate(self):

        global CONSTANT

        url_validate = "http://test.console.xqshijie.com/customer/validate/"+str(self.customer_phone)+".json"
        # print(url_validate)
        try:
            response = self.req_session.get(str(url_validate),headers = {'Authorization':self.bese_str})
            self.ismicroseconds = str(response.elapsed.microseconds)
            self.isjson = str(json.dumps(response.json(),ensure_ascii=False))
            self.istrue = str(json.dumps(response.json()['error'],ensure_ascii=False))
            self.isdata = str(json.dumps(response.json()['data'],ensure_ascii=False))
            self.iscode = str(json.dumps(response.json()['code'],ensure_ascii=False))
            self.ismessage = str(json.dumps(response.json()['message'],ensure_ascii=False))

            if  self.strassert in str(json.dumps(response.json()['code'],ensure_ascii=False)):
                self.isassert = str("符合预期")
            else:
                self.isassert = str("不符合,预期code返回： ")+str(self.strassert)
            if (len(self.args )>0):
                print(self.isjson,self.istrue,self.isdata,self.iscode,self.ismessage,self.isassert,self.args[0],self.customer_phone,' ',str(self.ismicroseconds)+"毫秒",str(CONSTANT)+'/'+str(self.numberMax))
                rwxls(self.getxls,self.number,self.istrue,self.isdata,self.iscode,self.ismessage,self.isassert,self.customer_phone,str(self.ismicroseconds),self.args[0])
            else:
                print(self.isjson,self.istrue,self.isdata,self.iscode,self.ismessage,self.isassert,self.customer_phone,' ',str(self.ismicroseconds)+"毫秒",str(CONSTANT)+'/'+str(self.numberMax))

                rwxls(self.getxls,self.number,self.istrue,self.isdata,self.iscode,self.ismessage,self.isassert,self.customer_phone,str(self.ismicroseconds))
        except :

            if (len(self.args)> 0):
                rwxls(self.getxls,self.number,'--','--','--','--','--',self.customer_phone,'--',self.args[0])
            else:
                rwxls(self.getxls,self.number,'--','--','--','--','--',self.customer_phone,'--')
            print(Exception.args,"访问接口失败",self.customer_phone,str(CONSTANT)+'/'+str(self.numberMax))

        if CONSTANT == self.numberMax:
            savexls(self.getxls,self.xlsname)
            print("完成")
        CONSTANT += 1
        sem.release()


if __name__ == '__main__':

    req_session,bese_str = gettoken()
    sqlconnect = Config.SqlConnect()
    xqsj_test = sqlconnect.get_xqsj_test_sql() #
    fangfull_test = sqlconnect.get_fangfull_test_sql()  #房否 test sql
    print("初始化完成")

    ###################### 房否
    #### 200 是老用户  602 没有订单  601 无效手机号
    #### '订单状态： 1已认购|2已取消|3已签约'
    # status = '3'
    # strsql = "select cu.customer_id,cu.customer_cellphone from customer cu where cu.customer_id in(select bka.coustomer_id from brokerage bka where bka.status = "+"'"+str(status)+"'"+") and cu.customer_cellphone != ''"
    # customerid,cellphone = sql_customer_cellphone_complex(strsql,fangfull_test)
    # getxls = openxls()
    # print("开始查询比对实际值")
    # maxThread = 10
    # sem=threading.BoundedSemaphore(maxThread-1)
    # for i in range(len(cellphone)):
    #     sem.acquire()
    #     t = RequestThread(req_session,bese_str,cellphone[i],'200',getxls,i,len(cellphone),'房否后台_老用户(多)',customerid[i]).start()





    #print('========================================')
    ##  已取消订单的用户不算老用户
    # strsql = "select cu.customer_id,cu.customer_cellphone from customer cu inner join ( SELECT bka.coustomer_id as coustomer_id FROM brokerage bka WHERE bka.STATUS = 1 or bka.STATUS = 2 and bka.coustomer_id not in ( select bkage.coustomer_id from brokerage bkage where bkage.STATUS = 3 ) ) ggg on cu.customer_id = ggg.coustomer_id limit 100,256"
    # customerid,cellphone = sql_customer_cellphone_complex(strsql,fangfull_test)
    # # print(len(cellphone))
    # getxls = openxls()
    # print("开始查询比对实际值")
    # maxThread = 10
    # sem=threading.BoundedSemaphore(maxThread-1)
    # for i in range(len(cellphone)):
    #     sem.acquire()
    #     t = RequestThread(req_session,bese_str,cellphone[i],'602',getxls,i,len(cellphone),'房否后台_已认购or已取消(多)',customerid[i]).start()


     ## 房否订单表中的新奇世界-成交客户
    # strsql = "select coustomer_id,xqsj_phone from brokerage where xqsj_phone != '' and status = '3'"
    # cellphone = get_readxls("D:\Backup\桌面\工作簿1.xlsx",'Sheet1',6)
    # customerid = get_readxls("D:\Backup\桌面\工作簿1.xlsx",'Sheet1',7)
    # print(customerid)
    # print(cellphone)
    # print(customerid)
    # customerid,cellphone = sql_customer_cellphone_complex(strsql,fangfull_test)
    # getxls = openxls()
    # print("开始查询比对实际值")
    # maxThread = 10
    # sem=threading.BoundedSemaphore(maxThread-1)
    # for i in range(len(cellphone)):
    #     sem.acquire()
    #     t = RequestThread(req_session,bese_str,cellphone[i],'200',getxls,i,len(cellphone),'房否后台_新奇世界_老客户(多)',customerid[i])
    #     t.start()
    # #

    # ## 房否订单表中的新奇世界-非成交客户
    # strsql = "select coustomer_id,xqsj_phone from brokerage where status != '3' and xqsj_phone != '' and coustomer_id not in (select br.coustomer_id from brokerage br where br.status = '3' and br.xqsj_phone != '')"
    # customerid,cellphone = sql_customer_cellphone_complex(strsql,fangfull_test)
    # getxls = openxls()
    # print("开始查询比对实际值")
    # maxThread = 10
    # sem=threading.BoundedSemaphore(maxThread-1)
    # for i in range(len(cellphone)):
    #     sem.acquire()
    #     t = RequestThread(req_session,bese_str,cellphone[i],'602',getxls,i,len(cellphone),'房否后台_新奇世界_已认购or已取消(多)',customerid[i]).start()


    # 房否后台没有订单记录的客户
    # strsql = "select ct.customer_id,ct.customer_cellphone from customer ct where ct.customer_cellphone !='' and ct.customer_id not in (select br.coustomer_id from brokerage br) order by ct.customer_id"
    # customerid,cellphone = sql_customer_cellphone_complex(strsql,fangfull_test)
    # # customerid = ['40404']
    # # cellphone = ['13127115988']
    # getxls = openxls()
    # print("开始查询比对实际值")
    # maxThread = 10
    # sem=threading.BoundedSemaphore(maxThread-1)
    # for i in range(len(cellphone)):
    #     sem.acquire()
    #     t = RequestThread(req_session,bese_str,str(cellphone[i]).replace(' ',''),'602',getxls,i,len(cellphone),'房否后台_没有订单记录的用户（多）',customerid[i]).start()

    # 200 是老用户  602 没有订单  601 无效手机号
    ## 房否后台没有订单记录的客户
    # strsql = "select ct.customer_id,ct.customer_cellphone from customer ct where ct.customer_cellphone !='' and ct.customer_id not in (select br.coustomer_id from brokerage br) order by ct.customer_id LIMIT 1,10000"
    # customerid,cellphone = sql_customer_cellphone_complex(strsql,xqsj_test)
    # getxls = openxls()
    # maxThread = 10
    # sem=threading.BoundedSemaphore(maxThread-1)
    # for i in range(len(cellphone)):
    #     sem.acquire()
    #     t = RequestThread(req_session,bese_str,cellphone[i],'602',getxls,i,len(cellphone),'测试多线程',customerid[i]).start()


# ## 新奇世界非老用户
#     strsql = "select DISTINCT(u.member_mobile) from uc_member u where u.member_id not in (select f.customer_id from fq_fenquan_order f where f.status = 1 and f.order_status = 2) and u.member_mobile != ''"
#     cellphone = sql_customer_cellphone(strsql,xqsj_test)
#     customerid = [1]*len(cellphone)
#     # cellphone = get_readxls("D:\Backup\桌面\房否新用户错误测试结果返回.xlsx",'Sheet1',7)
#     # customerid = get_readxls("D:\Backup\桌面\房否新用户错误测试结果返回.xlsx",'Sheet1',6)
#     getxls = openxls()
#     maxThread = 10
#     sem=threading.BoundedSemaphore(maxThread-1)
#     for i in range(len(cellphone)):
#         sem.acquire()
#         t = RequestThread(req_session,bese_str,str(cellphone[i]).replace(' ',''),'602',getxls,i,len(cellphone),'新奇世界_非老用户',customerid[i]).start()


## 新奇世界老用户
    # strsql = "select u.member_id,u.member_mobile from uc_member u where u.member_id in (select f.customer_id from fq_fenquan_order f where f.status = 1 and f.order_status = 2)and u.member_mobile != ''"
    # customerid,cellphone = sql_customer_cellphone_complex(strsql,xqsj_test)
    #
    # getxls = openxls()
    # maxThread = 10
    # sem=threading.BoundedSemaphore(maxThread-1)
    # for i in range(len(cellphone)):
    #     sem.acquire()
    #     t = RequestThread(req_session,bese_str,cellphone[i],'200',getxls,i,len(cellphone),'新奇世界_老用户',customerid[i])
    #     t.start()



    # customerid = ['1317']
    # cellphone = ['13001170890']
    # getxls = openxls()
    # maxThread = 10
    # sem=threading.BoundedSemaphore(maxThread-1)
    # for i in range(len(cellphone)):
    #     sem.acquire()
    #     t = RequestThread(req_session,bese_str,cellphone[i],'200',getxls,i,len(cellphone),'房否新客户',customerid[i])
    #     t.start()

    #
    # customerid = ['59317']
    # cellphone = ['15011111133']
    # getxls = openxls()
    # maxThread = 10
    # sem=threading.BoundedSemaphore(maxThread-1)
    # for i in range(len(cellphone)):
    #     sem.acquire()
    #     t = RequestThread(req_session,bese_str,cellphone[i],'602',getxls,i,len(cellphone),'明源签约_李岳_15011111133_房否',customerid[i])
    #     t.start()
    #
    customerid = ['未知']
    cellphone = ['13680000252']#13680000226
    getxls = openxls()
    maxThread = 10
    sem=threading.BoundedSemaphore(maxThread-1)
    for i in range(len(cellphone)):
        sem.acquire()
        t = RequestThread(req_session,bese_str,cellphone[i],'602',getxls,i,len(cellphone),'全房新13680000252',customerid[i])
        t.start()



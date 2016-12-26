# -*- coding:utf-8 -*-
#!/usr/bin/python

import re
import time

from bs4 import BeautifulSoup

import tools_request
from Fangfull.controller import User_login
from config import Config

# 类说明：案场订单录入员相关操作
#佣金信息表 brokerage


# 添加电商团购付款
def savePaymentRecord_tuangou(ipblue,cookies,brokerage_id):
    url = str(ipblue)+'manager/SavePaymentRecord'
    parameter = {
        #1非贷款类房款 1 楼款
        # 其他4 #电商团购费 22
        'brokerage_id':brokerage_id,
        'pay_amount_type':'4',   # 其他4
        'pay_nature':'22', #电商团购费 22
        'pay_amount':'8000',
        'confirm_pay_amount':'8000',
        'pay_ratio':'0.2857',
        'pay_date':time.strftime("%Y-%m-%d"),
        'pay_type':'1',
    }
    Content = tools_request.post_Request(url,parameter,cookies=cookies)
    print (Content)
    payment_id ,money = searchbrokeragr_paymentId(cookies,brokerage_id,False)
    return payment_id
# 添加楼款付款
def savePaymentRecord_loukuan(ipblue,cookies,brokerage_id):
    url = str(ipblue)+'manager/SavePaymentRecord'
    payment_id ,money= searchbrokeragr_paymentId(cookies,brokerage_id,False)
    parameter = {
        #1非贷款类房款 1 楼款
        # 其他4 #电商团购费 22
        'brokerage_id':brokerage_id,
        'pay_amount_type':'1',   # 非贷款类房款
        'pay_nature':'2', # 楼款
        'pay_amount':money,
        'confirm_pay_amount':money,
        'pay_ratio':'100',
        'pay_date':time.strftime("%Y-%m-%d"),
        'pay_type':'1',
    }
    tools_request.post_Request(url,parameter,cookies=cookies)
    payment_id ,money = searchbrokeragr_paymentId(cookies,brokerage_id,False)
    return payment_id

## 搜索用户订单，返回订单ID
def searchbrokeragr_brokerageId(ipblue,cookies,phone):
    url = str(ipblue)+'manager/searchbrokeragr'
    parameter = {
        'customer_name':'',
        'cell_phone':str(phone),
        'order_date':'',
        'building':'',
        'brokercompany_name':'',
        'brokerage_no':'',
        'xqsj_order_bm':'',
        'yt0':'搜 索',
    }
    Content = tools_request.post_Request(url,parameter,cookies=cookies)
    print (Content)
    # 获取
    brokerage_id = re.findall(r'/manager/updatebrokerage/id/(\w+)/bw_id//lid/1\?urls=/manager/searchbrokeragr" class="formNedit',Content)[0]

    return brokerage_id

# 查询缴费信息，返回付款序号ID 和楼盘总价 ,False返回最后一个订单序号，True返回所有未到账的订单序号
def searchbrokeragr_paymentId(ipblue,cookies,brokerage_id,isAll):
    url = str(ipblue) + 'manager/updatebrokerage/id/'+str(brokerage_id)+'/bw_id//lid/1?urls=/manager/searchbrokeragr'
    Content = tools_request.request_get(url,None,cookies=cookies)

    payment_id = re.findall(r'"/manager/deleteMoney/brokerage_id/'+str(brokerage_id)+'/id/(\w+)"',Content)
    soup = BeautifulSoup(Content, 'html.parser')
    text_money = soup.table
    # print ("2-------------")
    # print (text_money)
    # print ("3-------------")
    money = re.findall(r'协议总价：</span><\em>(\w+)',str(text_money))
    if isAll:
        return payment_id
    else:
        return payment_id[len(payment_id)-1],money
#删除付款金额
def deleteMoney(ipblue,cookies,brokerage_id,payment_id):
    url = str(ipblue) + '/manager/deleteMoney/brokerage_id/'+str(brokerage_id)+'/id/'+str(payment_id)
    tools_request.request_get(url,None,cookies=cookies)

# 订单录入员：发起团购结佣申请
def Groupbuy_status2(ipblue,cookies,brokerage_id):
    url = str(ipblue) + 'manager/Groupbuy_status2'
    parameter = {
        'brokerage_id':brokerage_id
    }
    tools_request.post_Request(url,parameter,cookies=cookies)

# 案场财务：付款审核通过，确认进账
def FinanceConfirmAmountIncome(ipblue,cookies,brokerage_id,payment_id):
    time.sleep(2)
    url = str(ipblue) + 'manager/FinanceConfirmAmountIncome'
    parameter = {
        'brokerage_id':brokerage_id,
        'payment_id':payment_id,
    }
    tools_request.post_Request(url,parameter,cookies=cookies)

# 总部财务审核团购费结佣
def GroupBuyFinanceApproveSettlementBrokerage(ipblue,cookies,brokerage_id):
    url = str(ipblue) + "manager/GroupBuyFinanceApproveSettlementBrokerage"
    parameter = {
        'brokerage_id':brokerage_id,
        'type_id':'1',#审核通过
    }
    tools_request.post_Request(url,parameter,cookies=cookies)

if __name__ == '__main__':

    # ip = Config.Ip()
    # ip.set_Ipblue('http://test1www.xqshijie.com/')
    # ip.set_Ipred('http://test2www.xqshijie.com/')
    # ip_blue = ip.get_Ipblue()
    # ip_red = ip.get_Ipred()


    ip = Config.Ip()
    ip.set_Ipblue('http://betawww.fangfull.com/')
    ip.set_Ipred('http://betaerp.fangfull.com/')
    ip_blue = ip.get_Ipblue()
    ip_red = ip.get_Ipred()
    sqlconnect = Config.SqlConnect()
    sqlMysql = sqlconnect.get_fangfull_beta_sql()

    phone = '13120000001'
    # 前提是名源提交用户订单
    print(ip_blue)
    acddlry_cookies = User_login.acddlry_login_red(ip_red) #登录案场订单录入员
    brokerage_id = searchbrokeragr_brokerageId(ip_blue,acddlry_cookies,phone)# 搜索用户订单，返回订单ID
    payment_id_tuangou = savePaymentRecord_tuangou(ip_blue,acddlry_cookies,brokerage_id) # 添加电商团购付款
    payment_id_loukuan = savePaymentRecord_loukuan(ip_blue,acddlry_cookies,brokerage_id)# 添加楼款
    accw_cookies = User_login.accw_login_red(ip_red)  # 登录案场财务
    FinanceConfirmAmountIncome(ip_blue,accw_cookies,brokerage_id,payment_id_tuangou)# 团购付款审核通过，确认进账
    FinanceConfirmAmountIncome(ip_blue,accw_cookies,brokerage_id,payment_id_loukuan)# 楼款付款审核通过，确认进账
    Groupbuy_status2(ip_blue,acddlry_cookies,brokerage_id)  # 订单录入员：发起团购结佣申请
    zbcw_cookis = User_login.zbcw_login_red(ip_red) # 登录总部财务
    GroupBuyFinanceApproveSettlementBrokerage(ip_blue,zbcw_cookis,brokerage_id) # 总部财务审核团购费结佣


    # dele_payment_id = searchbrokeragr_paymentId(acddlry_cookies,brokerage_id,True)
    # for i in range(len(dele_payment_id)):
    #     deleteMoney(acddlry_cookies,brokerage_id,dele_payment_id[i])





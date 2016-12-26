# -*- coding:utf-8 -*-
#!/usr/bin/python

import tools_request
import pprint
from config import Config
import tools_mysql
sql_connect = Config.app_test_sql()

#一：分页查询所有的逸乐通项目
def allPageProjects():
    url = Config.IP_APP +'xqsj/app/projects/allPageProjects.do'
    sql_project_name = tools_mysql.MysqlConnect('select project_name from project ORDER BY project_id DESC LIMIT 1',sql_connect)[0] #查询一条值
    print(sql_project_name)
    sel_projectid_count = tools_mysql.MysqlConnect('select COUNT(project_id) from project',sql_connect)

    parameter = [{'showCount':'-1', 'currentPage':'1'},##00 请求失败
        {'showCount':'z', 'currentPage':'1'},##00 请求失败
        {'showCount':'1', 'currentPage':'1'},#01 请求成功
        {'showCount':'00', 'currentPage':'1'},#02 返回空值
        {'showCount1':'','currentPage':''},#03 请求协议参数不完整(showCount)
        {'showCount':'','currentPage1':''},#03 请求协议参数不完整(currentPage)
        ]
    #00 请求失败
    return_json = tools_request.Request_postApp(url,parameter[0])
    tools_request.Assert('00',return_json['result'],1)
    #00 请求失败
    return_json = tools_request.Request_postApp(url,parameter[1])
    tools_request.Assert('00',return_json['result'],1)
    #01 请求成功
    return_json = tools_request.Request_postApp(url,parameter[2])
    tools_request.Assert(str(sql_project_name[0]),str(return_json['datas'][0]['project_name']),1)
    #02 返回空值
    if sel_projectid_count[0] == 0 :
        return_json = tools_request.Request_postApp(url,parameter[3])
        tools_request.Assert('02',return_json['result'],1)
    #03 请求协议参数不完整
    return_json = tools_request.Request_postApp(url,parameter[4])
    tools_request.Assert('03',return_json['result'],1)

#二：逸乐通规格弹层选择页
def getByProjectId():
    # bug : 接口返回的状态值是code 其他 的接口返回值是 result
    url = Config.IP_APP + 'xqsj/app/projects/getByProjectId'
    parameter = {'project_id':'1'}
    return_json = tools_request.Request_postApp(url,parameter)
    print (return_json)

#三：我的钱包
def mycashlist():
    # Bug ：不登录也能通过ID查询出结果
    url = Config.IP_APP +'xqsj/app/cash/mycashlist.do'
    parameter = {'customer_id':'3'}
    return_json = tools_request.Request_postApp(url,parameter)
    print (return_json)

# 四：逸乐通首页面（流程及首页面banner图一个接口，动态的产品列表是接口一）
def getConfig():
    url = Config.IP_APP + 'xqsj/app/projects/getConfig.do'
    return_json = tools_request.Request_postApp(url,None)
    print(return_json)
# 五：获取支付渠道列表
def paychannellist():
    url = Config.IP_APP + 'xqsj/app/paychannel/paychannellist.do'
    return_json = tools_request.Request_postApp(url,None)
    print(return_json)
# 六：我的订单
def myorderlistpage():
    url = Config.IP_APP + 'xqsj/app/order/myorderlistpage.do'
    sql_customer_id,sql_cusomter_name = tools_mysql.MysqlConnect( 'select customer_id,cusomter_name FROM fq_fenquan_order where STATUS = 1 ORDER BY order_id DESC LIMIT 1',sql_connect)[0]

    parameter = {
        'customer_id':sql_customer_id,
        'currentPage':'1',
        'showCount':'20'
    }
    return_json = tools_request.Request_postApp(url,parameter)
    pprint.pprint (return_json)

# 七：订单详情
def orderdetails():
    url = Config.IP_APP + 'xqsj/app/order/orderdetails.do'
    parameter = {
        'order_id':'1453',
    }
    return_json = tools_request.Request_postApp(url,parameter)

# 八：订单详情-我的支付记录
def mypaymentlist():
    order_id,count= tools_mysql.MysqlConnect("select b.order_id, count(b.order_id) cnt from fq_fenquan_payment b where b.order_id in (select a.order_id from fq_fenquan_order a  ) group by b.order_id having count(b.order_id) >1 LIMIT 1",sql_connect)[0]
    Array_sql = tools_mysql.MysqlConnect("select ffp.payment_id from fq_fenquan_order ffo INNER JOIN fq_fenquan_payment ffp on ffo.order_id = ffp.order_id where ffo.order_id = "+str(order_id),sql_connect)
    payment_id = []
    for i in range (len(Array_sql)):
        payment_id.append(Array_sql[i][0])

    url = Config.IP_APP+'xqsj/app/order/mypaymentlist.do'
    parameter = {
        'order_id':order_id,
    }
    return_json = tools_request.Request_postApp(url,parameter)
    tools_request.Assert(len(payment_id),len(return_json['payments']),0,describe = "断言描述:判断查询结果返回的 len 是一致的")
    tools_request.Assert(str(order_id),str(return_json['payments'][0]['order_id']),0,describe = "断言描述:判断查询结果的 order_id 与 传递查询的order_id是一致的")
    pprint.pprint (return_json)

#九：订单详情--支付页面所需数据
def detail():
    url = Config.IP_APP+'xqsj/app/order/detail'
    # order_status 1|待付款,2|已付清,4|待付余款,21|已关闭(历史订单),100|已取消,101|已关闭(超时),105|退款审核中,107|已退款,108|退款审核未通过,109|退款审核通过待退款'
    # 待付款
    #order_id 订单id ，all_pay_price 已支付订单总金额  order_display_id 长订单ID
    order_id_wait_payment,all_pay_price,order_display_id= tools_mysql.MysqlConnect("select order_id,all_pay_price,order_display_id from fq_fenquan_order as ffo WHERE (ffo.order_status = 1) and (ffo.payment_method = 1) and (ffo.status = 1) ORDER BY ffo.order_id desc LIMIT 1",sql_connect)[0]
    parameter_wait_payment ={'order_id':order_id_wait_payment}
    return_wait_payment_json = tools_request.Request_postApp(url,parameter_wait_payment)
    tools_request.Assert(order_id_wait_payment,return_wait_payment_json['data']['order_id'],0,describe='描述：待付款订单订单 ID 与接口返回订单订单 ID 是否相同')
    tools_request.Assert(float(all_pay_price),float(return_wait_payment_json['data']['all_pay_price']),0,describe='描述：待付款已支付订单总金额 与 接口已支付订单总金额是否相等')
    tools_request.Assert(order_display_id,return_wait_payment_json['data']['order_display_id'],0,describe='描述：待付款长订单ID 与 接口长订单ID是否相等')
    print (return_wait_payment_json)
    # print(return_wait_payment_json)


    #已付清
    order_id_fully_paid,all_pay_price,order_display_id= tools_mysql.MysqlConnect("select order_id,all_pay_price,order_display_id from fq_fenquan_order as ffo WHERE (ffo.order_status = 2) and (ffo.payment_method = 1) and (ffo.status = 1) ORDER BY ffo.order_id desc LIMIT 1",sql_connect)[0]
    #待付余款
    order_id_residual_payment,all_pay_price,order_display_id = tools_mysql.MysqlConnect("select order_id,all_pay_price,order_display_id from fq_fenquan_order as ffo WHERE (ffo.order_status = 4) and (ffo.payment_method = 1) and (ffo.status = 1) ORDER BY ffo.order_id desc LIMIT 1",sql_connect)[0]
    #已取消
    order_id_countermand,all_pay_price,order_display_id= tools_mysql.MysqlConnect("select order_id,all_pay_price,order_display_id from fq_fenquan_order as ffo WHERE (ffo.order_status = 100) and (ffo.payment_method = 1) and (ffo.status = 1) ORDER BY ffo.order_id desc LIMIT 1",sql_connect)[0]


    # parameter__fully_paid ={'order_id':order_id_fully_paid}
    # return_fully_paid_json = tools_request.Request_postApp(url,parameter__fully_paid)
    # print(return_fully_paid_json)
    #
    # parameter_residual_payment ={'order_id':order_id_residual_payment}
    # return_residual_payment_json = tools_request.Request_postApp(url,parameter_residual_payment)
    # print(return_residual_payment_json)
    #
    # parameter_countermand ={'order_id':order_id_countermand}
    # return_countermand_json = tools_request.Request_postApp(url,parameter_countermand)
    # print(return_countermand_json)


# 十：增加订单说明
def saveOrder():
    url = Config.IP_APP+'xqsj/app/order/saveOrder'
    parameter = {'customer_id':'38',
                 'cusomter_name':'',
                 'cusomter_phone':'',
                 'item_quantity':'1',
                 'item_id':'17',
                 'final_price':'1',
                 'item_price':'1',
                 'introducer_code':'',	#string	推荐人手机号或者机构标识码 (必填)
                'introducerType':'1',#1=机构推荐，2=个人推荐 (必填)
                 }
    return_json = tools_request.Request_postApp(url,parameter)
    print(return_json)

if __name__ == "__main__":

    # allPageProjects()
    # getByProjectId()
    # mycashlist()
    # getConfig()
    # paychannellist()
    # myorderlistpage()
    mypaymentlist()
    # detail()
    # saveOrder()


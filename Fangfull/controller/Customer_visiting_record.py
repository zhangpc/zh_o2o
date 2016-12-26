# -*- coding:utf-8 -*-
#!/usr/bin/python
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
import json
import re,time,datetime,bs4
from config import Config
import tools_request
import tools_mysql
from Fangfull.controller import User_login


# sql_connect = Config.sql_connect(Config.sql_index).set_connect()


# 查询案场客服审核用户时的ID
def getVisitAuditList(ipred,cookies,phone):
    time.sleep(2)
    # time.strftime('%Y-%M-%d')
    url = str(ipred)+'admin.php?r=product/VisitAudit/VisitAuditList&group[customer_name]=&group[status]=&group[start_time]=&group[end_time]=&group[customer_cellphone]='+str(phone)
    Content = tools_request.request_get(url,None,cookies=cookies)
    try :
        re_input_id = re.findall(r'r=product/VisitAudit/VisitAudit&id=(\w+)',Content)[0]
        print('案场客服找到要进行到访审核的客户，返回ID'+str(re_input_id))
        return re_input_id
    except:
        print('案场客服没找到要进行到访审核的客户')
        return None
    # print (re_input_id)


# 到访审核通过
def VisitAudited(ipred,cookies,VisitAudit_id):
    time.sleep(2)
    url_token =str(ipred)+"admin.php?r=product/VisitAudit/VisitAudit&id="+str(VisitAudit_id)
    centent = tools_request.request_get(url_token,None,cookies=cookies)
    soup = bs4.BeautifulSoup(centent,'html.parser')
    get_input_all = soup.find_all('input')
    get_token = re.findall('<input name="token" type="hidden" value="(\w+)',str(get_input_all))[0]


    url = str(ipred)+'admin.php?r=product/VisitAudit/VisitAudited'
    parameter = {
        'id':str(VisitAudit_id),
        'VisitAudit[audit_status]':'2',
        'VisitAudit[audit_content]':'备注：自动化添加到访审核通过,客户ID是'+str(VisitAudit_id),
        'token':str(get_token),
        'yt0':'保 存',
    }
    print("准备进行到访审核")
    centent = tools_request.post_Request(url,parameter,cookies=cookies)
    print('到访审核通过')

# 添加用户到访
def customerVisitingRecord(ipblue,cookies,userid,phone,isExpire,building_id,building_name,sql_connect):
    get_customerVisitingRecord_url = str(ipblue)+"customerVisitingRecord/createVisitingRecord/id/"+str(userid)+"?urls=/managerCustomer/customerVisit/customer_cellphone/"+str(phone)
    post_customerVisitingRecord_url = str(ipblue)+"customerVisitingRecord/saveVisitingRecord?urls=/managerCustomer/customerVisit/customer_cellphone/"+str(phone)
    get_customerVisitingRecord_text_token = tools_request.request_get(get_customerVisitingRecord_url,None,cookies=cookies)

    re_input_token = re.findall(r'<input type="hidden" name="savevisitingRecord_token" value="(\w+)" />',get_customerVisitingRecord_text_token)
    # img = r'./123.png'
    # img = "..\\static\\img\\test_visit_commit_img.png"
    # openimg = open(img,'rb')
    buildingIdandName = "'"+str(building_id)+','+str(building_name)+"'"
    buildingIdandName = buildingIdandName.replace("\'",'')
    # print(building_name)
    # time.strftime("%Y-%m-%d %H:%M",time.localtime())


    visiting_date = time.strftime("%Y-%m-%d",time.localtime())
    # print(visiting_date)
    parameter = {
        'savevisitingRecord_token':re_input_token[0],
        'visitingRecord[customer_id]':userid,
        'visitingRecord[visiting_date]':visiting_date,
        'visitingRecord[visit_type]':'2',
        'visitingRecord[age]':'2',
        'visitingRecord[job]':'1',
        'visitingRecord[live_spaces]':'1001001',
        'visitingRecord[product_intent]':'2',
        'visitingRecord[intent_form]':'2',
        'visitingRecord[intent_payment_type]':'1',
        'visitingRecord[intent_total_price]':'1',
        'visitingRecord[purchase_factors]'	:'1',
        'visitingRecord[distribution_channel]':'1',
        'visitingRecord[cognitive_channel]':'2',
        'visitingRecord[follow_up_stage]':'1',
        'visitingRecord[customer_grade]':'1',
        'visitingRecord[work_spaces]':'1001001',
        'visitingRecord[purchase_purpose]'	:'1',
        'visitingRecord[intent_house_type]':'1',
        'visitingRecord[intent_area]':'1',
        'visitingRecord[intent_unit_price]':'2',
        'visitingRecord[purchase_resistance_factor]':'1',
        'visitingRecord[location_name]':buildingIdandName,#',北京中弘大厦',#'24,北京中弘大厦' #100,中弘广场
        'visitingRecord[visit_commit_img]':'E:\文档\svn文档\自动化\Myproject\Fangfull\static\img\test_visit_commit_img.png',
        'visitingRecord[remark]':'',
        'yt0':'保 存',
    }
    if isExpire == False:
        print("从数据库获取用户在小绑表中存的ID和录入时间")
        broker_vie_customer_id,begin_time = tools_mysql.MysqlConnect("select id,begin_time from broker_netin_customer  where customer_id = " +str(userid)+  " ORDER BY id desc LIMIT 1",sql_connect)[0]

        change_begin_time = begin_time - datetime.timedelta(hours = 1)
        # print (change_begin_time)
        # print(type(change_begin_time))
        # print (broker_vie_customer_id,'    ',userid)
        print("给客户报备时间往前提前一个小时")
        tools_mysql.MysqlConnect("UPDATE broker_netin_customer set begin_time = "+'"'+str(change_begin_time.strftime("%Y-%m-%d %H:%M:%S"))+'"'+" where customer_id = "+ str(userid) +" and id = "+str(broker_vie_customer_id),sql_connect)
    print("添加客户到访")
    tools_request.post_Request(post_customerVisitingRecord_url,parameter,cookies=cookies)

    # 上传图片，暂时没用上
def upload_index(ipblue,cookies):
    url = str(ipblue)+"upload/index"
    parameter = {
        'Content-Disposition: form-data; name="filetype"':'12',
        'Content-Disposition: form-data; name="control"':'visitingRecord_visit_commit_img',
        'Content-Disposition: form-data; name="fileup"; filename="E:\\Work\\Myproject\\Request\\concurrent\\123.png" Content-Type: image/png':'<file>',
    }
    tools_request.post_Request(url,parameter,cookies=cookies)

#项目总监分配分销未成交客户给置业顾问（案场客服）
def post_submitDistribute(ipblue,cookies,customer_id,employee_id,building_id,building_name,customer_grade):
    url = str(ipblue)+'admin.php?r=product/managerCustomer/submitDistribute'
    parameter = {
        'customer_id':str(customer_id),
        'building_id':str(building_id),
        'employee_id':str(employee_id),
        'building_name':str(building_name),
        'customer_grade':str(customer_grade),
    }
    content = tools_request.post_Request(url,parameter,cookies=cookies)
    try:
        content = json.loads(content)
        if content['code'] == 1:
            print('项目总监分配客户成功')
    except:
        print('项目总监分配客户失败')
    return content
# 客户预约查询
def get_myReserveList(ipblue,cookies,building_id,customer_id,customer_cellphone,appointment_status,sql_connect):
    url = str(ipblue) +'customerAppointment/myReserveList'
    centent = tools_request.request_get(url,None,cookies=cookies)
    soup = bs4.BeautifulSoup(centent,'html.parser')
    get_td_all = soup.find_all('td')
    message_all = re.findall('<td>(\w+)</td>',str(get_td_all))
    # print(message_all)
    isexistence = False
    for message in message_all:
        if customer_cellphone in message:
            isexistence = True
    if isexistence == True:
        appointmentid,buildingid,status = tools_mysql.MysqlConnect("select appointment_id,building_id,status from customer_appointment where customer_id = "+str(customer_id),sql_connect)[0]
        if(str(buildingid) == str(building_id)) and str(appointment_status) == str(status):
            print("sql查询反馈 - 预约信息查询结果，预约ID是 ",appointmentid," 楼盘ID：",building_id," 状态：",status)
            return appointmentid
        else:
            print("sql查询反馈 - 预约的楼盘或状态有错，预约ID是 ",appointmentid," 楼盘ID：",building_id," 状态：",status)
            return False
    else:
        print('查询的预约手机号不存在')
        return isexistence

# 客户预约
def customerAppointment_savebroker(ipblue,cookies,customer_id,customer_phone,building_id):
    url_getaddcreate = str(ipblue) + 'customerAppointment/addcreate'
    content_getadd = tools_request.request_get(url_getaddcreate,None,cookies=cookies)
    # print(content_getadd)
    #获取表单Token
    soup = bs4.BeautifulSoup(content_getadd,'html.parser')
    get_input_all = soup.find_all('input')
    broker_token = re.findall('<input name="savebroker_token" type="hidden" value="(\w+)"/>',str(get_input_all))[0]

    #获取当前时间
    nowtime = time.strftime("%Y-%m-%d %H:%M",time.localtime())
    #str 转时间格式后，往下推一天
    nexttime = datetime.datetime.strptime(nowtime,"%Y-%m-%d %H:%M") + datetime.timedelta(days = 1)
    params = {
        'CustomerAppointment[ids]':'0',
        'savebroker_token':str(broker_token),
        'CustomerAppointment[customer_id]':str(customer_id),
        'CustomerAppointment[building_id]':str(building_id),
        'CustomerAppointment[appoint_time]	':nexttime,
        'CustomerAppointment[appointed_by]	':'1',#由谁预约 1 客户自己，2经纪人
        'CustomerAppointment[appointed_type]':'1',#预约方式 1 客户自去，2经纪人带着去
        'CustomerAppointment[customer_grade]':'1',#客户意向等级  1 暂无意向，2 意向较弱 ，3 有可能买房 ，4 急需买房
        'CustomerAppointment[remark]':'自动化添加预约'+str(customer_phone),
        'yt0':'保 存',
    }
    url_savebroker = ipblue+'customerAppointment/savebroker'
    content_save = tools_request.post_Request(url_savebroker,params,cookies=cookies)

# 讲解员（置业顾问）查询楼盘下的预约信息（暂时没用到）
def get_BuildingNew(ipblue,cookies,building_id):
    url = str(ipblue) +'admin.php?r=product/appointment/BuildingNew/bid/'+str(building_id)
    content = tools_request.request_get(url,None,cookies=cookies)
    print(content)
## 提交预约状态为如期履约
def appointment_status_set(ipred,cookies,appointment_id,status):
    url = str(ipred) + 'admin.php?r=product/appointment/BuildingInfo/id/'+str(appointment_id)
    params = {
        'status':str(status),
        'remark':'预约备注',
    }
    content = tools_request.post_Request(url,params,cookies=cookies)
    if str(status) == '1':
        print("讲解员确认预约，预约状态改变为:预约" )
    elif str(status) == '2':
        print("讲解员确认预约，预约状态改变为:确认" )
    elif str(status) == '3':
        print("讲解员确认预约，预约状态改变为:如期履约" )
    elif str(status) == '4':
        print("讲解员确认预约，预约状态改变为:爽约")
    elif str(status) == '5':
        print("讲解员确认预约，预约状态改变为:取消")

if __name__ == '__main__':
    phone = '13600021029'
    # ackf_cookies = User_login.ackf_login_blue()
    # VisitAudit_id = getVisitAuditList(ackf_cookies,phone)
    # VisitAudited(ackf_cookies,VisitAudit_id)

    # aa = "UPDATE broker_netin_customer set begin_time = "+'"'+str(change_begin_time.strftime("%Y-%m-%d %H:%M:%S"))+'"'+" where customer_id = "+ str(userid) +" and id = "+str(broker_vie_customer_id)
    # print(aa)
    xmzj_cookies = User_login.xmzj_login_blue('http://test2www.xqshijie.com/','zcsxmzj')

    centent = post_submitDistribute('http://test2www.xqshijie.com/',xmzj_cookies,'1001378','2175','24','北京中弘大厦','3')
    print(centent)
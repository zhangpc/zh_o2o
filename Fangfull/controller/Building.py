# -*- coding:utf-8 -*-
#!/usr/bin/python
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

from config import Config
from Fangfull.controller import User_login
import tools_request
import re
import random
import bs4
import time
import tools_mysql
import datetime

# sql_connect = Config.sql_connect(Config.sql_index).set_connect()

# 上传图片
def upload_index(ipblue,cookies):
    file = "./static/img/test_visit_commit_img.png"
    parameter = {
        'Content-Disposition: form-data; name="filetype"':'11',
        'Content-Disposition: form-data; name="control"':'First_Image',
        'Content-Disposition: form-data; name="fileup";filename="..\\static\\img\\test_visit_commit_img.png" Content-Type: image/png':'<file>'
    }
    url = str(ipblue)+'/upload/index'
    Content = tools_request.post_Request(url,parameter,cookies = cookies)
    # print (Content)


# （1）创建项目
def Brokeragetem_create(ipred,cookies,item_code,item_name,sql_connect):

    # item_code  = '99'
    # item_name = 'python'

    url = str(ipred)+'admin.php?r=product/Brokeragetem/create'
    parameter={
        'Brokeragetem[item_code]':item_code,
        'Brokeragetem[item_name]':item_name,
    }
    Brokeragetem = tools_request.post_Request(url,parameter,cookies=cookies)

    print('项目创建___________[√]')

    item_id = tools_mysql.MysqlConnect("SELECT item_id from brokerage_item where item_code =" + "'"+str(item_code)+"'",sql_connect)[0][0]

    return Brokeragetem,item_id

# （2）创建楼盘，返回楼盘名称
def building_mysave(ipblue,cookies,item_id):
    getbuildingproperty_url = str(ipblue)+"building/mycreate"
    getbuildingproperty_token = tools_request.request_get(getbuildingproperty_url,None,cookies=cookies)
    soup = bs4.BeautifulSoup(getbuildingproperty_token, 'html.parser')
    all_list_input = soup.find_all('input')
    mysavebuilding_token = re.findall(r'<input name="mysavebuilding_token" type="hidden" value="(\w+)"/>',str(all_list_input))
    random_int = random.randint(0,1000)
    building_name = "AutoAPITest_楼盘名"+str(random_int)
    parameter = {
        'Building[ids]':'0',
        'mysavebuilding_token':mysavebuilding_token[0],
        'Building[building_name]':building_name,
        'Building[item_id]':str(item_id),
        'Building[building_province]':'2',
        'Building[building_city]':'2002',
        'Building[building_county]':'2002001',
        'Building[building_position]':'AutoAPITest_具体位置'+str(random_int),
        'Building[phone_code]':'022',
        'Building[building_phone]':'88888888',
        'Building_building_open_time_status':1,
        'Building[building_open_time]':time.strftime('%Y-%m-%d'),
        'Building_building_price_status':1,
        'Building[building_price]':2000,
        'Building[building_type]':35,
        'Building[building_property_type][]':48,
        'Building[building_build_type][]':44,
        'Building[building_area]':'5000',
        'Building[building_checkin_time]':time.strftime('%Y-%m-%d'),
        'Building_building_property_fee_status':'1',
        'Building[building_property_fee]':'2',
        'Building[building_district]':'AutoAPITest_楼盘所属区域',
        'Building[picture_url]':upload_index(ipblue,cookies),
        'Building[brokerage_min_percent]':50,
        'Building[building_description]':'AutoAPITest_楼盘描述',
        'upfile':'',
        'Building[building_content]':'',
        'Building[buliding_lo]':'',
        'Building[building_lat]':'',
        'Building[offline_room_card_code]':'0000000001',
        'yt0':'保 存',
    }
    url = str(ipblue)+'building/mysave'
    requests1 = tools_request.post_Request(url,parameter,cookies=cookies)

    print('楼盘创建___________[√]')

    return building_name

# （3）获取楼盘ID
def get_building_myowen(ipblue,cookies,building_name):
    url = str(ipblue)+'building/myowen'
    myowen = tools_request.request_get(url,None,cookies=cookies)

    soup = bs4.BeautifulSoup(myowen, 'html.parser')
    all_list_input = soup.find_all('tbody')
    # print (all_list_input)

    building_id = re.findall(r'<td>(\w+)</td>\s+<td>'+str(building_name)+'</td>',str(all_list_input))[0]
    print('building_id',building_id)
    return building_id


# （4）添加户型,返回户型名称
def buildinghouse_mysave(ipblue,cookies,item_code,building_id):

    # building_id = tools_mysql.MysqlConnect('select max(building_id) from building',sql_connect)
    getbuildinghouse_url = str(ipblue) + "/buildingHouse/mycreate/bcid/" + str(building_id)
    getbuildinghouse_token = tools_request.request_get(getbuildinghouse_url,None,cookies=cookies)

    soup = bs4.BeautifulSoup(getbuildinghouse_token, 'html.parser')
    all_list_input = soup.find_all('input')
    mysavebuildinghouse_token = re.findall(r'<input name="mysavebuildinghouse_token" type="hidden" value="(\w+)"/>',str(all_list_input))

    random_int = random.randint(0,1000)
    house_name = "AutoAPITest_户型" + str(random_int)

    parameter = {
        'mysavebuildinghouse_token': mysavebuildinghouse_token,
        'BuildingHouse[ids]':	'0',
        'BuildingHouse[building_id]':	str(building_id),
        'BuildingHouse[house_name]':	house_name,
        'BuildingHouse[house_type]':	'6',
        'BuildingHouse[house_areas]':	str(item_code),
        'BuildingHouse[house_picture]':	'/upload/20160803/201608031745001470217500.jpg',
        'BuildingHouse[status]':'1',
        'yt0':	'保 存'
    }

    url = str(ipblue)+'/buildingHouse/mysave'
    requ = tools_request.post_Request(url,parameter,cookies=cookies)
    print("house_name " , house_name)
    print('户型创建___________[√]')
    return house_name

# （5）创建楼栋
def XkBan_create(ipred,cookies,building_id,sql_connect):
    url = str(ipred)+'admin.php?r=product/XkBan/create'

    Referer = str(ipred) + 'admin.php?r=product/xkBan/index'
    random_int = random.randint(0,1000)
    banname = "AutoAPITest_楼栋" + str(random_int)

    parameter = {
        'REFERER': Referer,
        'XkBan[floorlist]':	'1,2,3',
        'XkBan[projectid]':	building_id,
        'XkBan[bancode]':	89757,
        'XkBan[banname]':	banname,
        'XkBan[architecturalnature]':	1,
        'XkBan[propertytype]':	1,
        'XkBan[buildpricetype]':	2,
        'XkBan[salestype]':	1,
        'XkBan[saleslicense]':'',
        'XkBan[salesstate]':	0,
        'XkBan[salestime]':	'2016-08-04',
        'XkBan[unitnumber]':	3,
        'XkBan[floornumber]':	3,
        'XkBan[roomcardnumber]':	12,
    }
    XkBan = tools_request.post_Request(url,parameter,cookies = cookies)

    # print (XkBan)
    banid = tools_mysql.MysqlConnect("select max(banid) from erp_xk_ban where projectid =" + str(building_id),sql_connect)[0][0]

    bancode = tools_mysql.MysqlConnect('select bancode from erp_xk_ban where banid = '+str(banid),sql_connect)[0][0]

    banname = tools_mysql.MysqlConnect('select banname from erp_xk_ban where banid = '+str(banid),sql_connect)[0][0]

    print('楼栋创建___________[√]')
    print(banid,bancode,banname)
    return banid,bancode,banname

# （6）创建房间

def XkBanunit(ipred,cookies,building_id,banid,bancode,banname,sql_connect):

    Refefer = 'admin.php?r=product/XkBanunit/index'+ '&banid=' + str(banid) + '&plsc=1'
    url_one = ipred + 'admin.php?r=product/XkBan/update&id=' + str(banid)

    param_one = {
        'REFERER':	Refefer,
        'XkBan[floorlist]':	'1,2,3',
        'XkBan[bancode]':	bancode,
        'XkBan[banname]':	banname,
        'XkBan[architecturalnature]':'1',
        'XkBan[propertytype]':	'1',
        'XkBan[buildpricetype]':	'2',
        'XkBan[rentaltype]':	'1',
        'XkBan[unitnumber]':	'3',
        'XkBan[floornumber]':	'3',
    }
    XkBanunit_1 = tools_request.post_Request(url_one,param_one,cookies = cookies )


    url_two = ipred + 'admin.php?r=product/XkBanunit/create'
    param_two = {
        'plsc[dy][1][0]':	'1单元',
        'plsc[dy][1][1]':	2,
        'plsc[dy][2][0]':	'2单元',
        'plsc[dy][2][1]':	2,
        'plsc[dy][3][0]':	'3单元',
        'plsc[dy][3][1]':	2,
        'plsc[lc][3]':	'3层',
        'plsc[lc][2]':	'2层',
        'plsc[lc][1]':	'1层',
        'REFERER':	'/admin.php?r=product/XkBanunit/index' + '&banid='+ str(banid) + '&unitnumber=3&floornumber=3&huxing=1',
        'building_id':	building_id,
        'banid':	banid,
        'dy':	3,
        'louceng':	3,
        'roomcardnumber':	12
    }
    XkBanunit_2 = tools_request.post_Request(url_two,param_two,cookies = cookies)
    # print (XkBanunit_2)

    TimeNow = datetime.datetime.now()
    timeStamp = int(time.mktime(TimeNow.timetuple()))
    url_erpapi_one = ipred + 'admin.php?r=erpapi/privateMessage/ajaxListInbox&callback=jQuery' + '1830033743141337294946_' + str(timeStamp)

    erpapi_param_one = {
        'page':	'1',
        'pageSize':	'3',
        'user_type':	'1',
        'user_id':	'450',
        'unread':	'true'
    }
    XKBan_API_1 = tools_request.post_Request(url_erpapi_one,erpapi_param_one,cookies = cookies)

    time.sleep(2)

    url_erpapi_two = ipred + 'admin.php?r=erpapi/privateMessage/ajaxListInbox&callback=jQuery' + '21105597726154270167_' + str(timeStamp)

    erpapi_param_two = {
        'page':	'1',
        'pageSize':	'3',
        'user_type':	'1',
        'user_id':	'450',
        'unread':	'true'
    }
    XKBan_API_2 = tools_request.post_Request(url_erpapi_two,erpapi_param_two,cookies = cookies)

    time.sleep(2)

    url_erpapi_three = ipred + 'admin.php?r=erpapi/privateMessage/ajaxListInbox&callback=jQuery' + '21106480583164943938_' + str(timeStamp)

    erpapi_param_three = {
        'page':	'1',
        'pageSize':	'3',
        'user_type':	'1',
        'user_id':	'450',
        'unread':	'true'
    }
    XKBan_API_3 = tools_request.post_Request(url_erpapi_three,erpapi_param_three,cookies = cookies)


    url_three = ipred + 'admin.php?r=product/XkBanunit/Create'

    param_three = {
        'end': '130'
    }

    XkBanunit_3 = tools_request.request_get(url_three,param_three,cookies = cookies)


    time.sleep(2)

    url_erpapi_four = ipred + 'admin.php?r=erpapi/privateMessage/ajaxListInbox&callback=jQuery' + '21106480583164943938_' + str(timeStamp)

    erpapi_param_four = {
        'page':	'1',
        'pageSize':	'3',
        'user_type':	'1',
        'user_id':	'450',
        'unread':	'true'
    }
    XKBan_API_4 = tools_request.post_Request(url_erpapi_four,erpapi_param_four,cookies = cookies)

    print('房间创建___________[√]')

    house_id = tools_mysql.MysqlConnect('select house_id from building_house where building_id = '+ str(building_id),sql_connect)[0][0]

    return house_id


# （7）新建卡类型
def roomCardType(ipred,item_id,cookies,sql_connect):
    random_int = random.randint(0,100)
    cardName = "APITest_卡名"+str(random_int)

    url = str(ipred)+'admin.php?r=product/roomCardTypeeckHouseIdExist'
    parameter={
        'pars[action]':	'checkHouseIdExist',
        'pars[project_id]':	str(item_id)
    }

    CardType = tools_request.post_Request(url,parameter,cookies=cookies)


    url_create = str(ipred)+'admin.php?r=product/roomCardType/create'
    param_create = {
        'RoomCardType[room_card_name]':	str(cardName),
        'RoomCardType[project_id]':	str(item_id),
        'RoomCardType[room_card_price]':	'1000',
        'RoomCardType[room_card_number]':	'100',
        'RoomCardType[room_card_surplus_number]':	'100',
        'RoomCardType[online_room_card_number]':	'100',
        'RoomCardType[online_surplus_number]':	'100'
    }

    cardcreate = tools_request.post_Request(url_create,param_create,cookies = cookies)

    TimeNow = datetime.datetime.now()
    timeStamp = int(time.mktime(TimeNow.timetuple()))
    url_erpapi = ipred + 'admin.php?r=erpapi/privateMessage/ajaxListInbox&callback=jQuery' + '21105597726154270167_' + str(timeStamp)

    erpapi_param = {
        'page':	'1',
        'pageSize':	'3',
        'user_type':	'1',
        'user_id':	'450',
        'unread':	'true'
    }
    cardcreate_api = tools_request.post_Request(url_erpapi,erpapi_param,cookies = cookies)

    room_card_typeid = tools_mysql.MysqlConnect('select room_card_type_id from erp_room_card_type where project_id ='+ str(item_id),sql_connect)[0][0]

    print('逸乐通卡类型创建成功___________[√]')


    return room_card_typeid


#新建卡
def createCardSave(ipred,cookies,item_code,room_card_typeid):

    # startnum = tools_mysql.MysqlConnect('select max(endnum) from erp_room_card_history where itemcode = '+"'"+str(item_code)+"'",sql_connect)[0][0]
    # startnum = tools_mysql.MysqlConnect('select max(endnum) from erp_room_card_history where itemcode = 07',sql_connect)[0][0]

    startnum = 0
    endnum = 100

    url = str(ipred) + '/admin.php?r=product/roomCardType/ifCardNumExist'

    param_card = {
        'item_code':	item_code,
        'startnum':	str(startnum),
        'endnum':	str(endnum)
    }

    CardExist = tools_request.post_Request(url,param_card,cookies = cookies)

    random_int = random.randint(0,100)
    house_name = "APITest_户型" + str(random_int)
    url_sava = str(ipred) + 'admin.php?r=product/roomCardType/createCardSave'

    param_save = {
        'CardType[roomcardtypeid]':	str(room_card_typeid),
        'CardType[cardname]':	str(house_name),
        'CardType[pin]':	'998888',
        'CardType[itemcode]':str(item_code),
        'CardType[start]':	str(startnum),
        'CardType[end]':	str(endnum)
    }

    CardSave = tools_request.post_Request(url_sava,param_save,cookies = cookies)

    TimeNow = datetime.datetime.now()
    timeStamp = int(time.mktime(TimeNow.timetuple()))
    url_erpapi = ipred + 'admin.php?r=erpapi/privateMessage/ajaxListInbox&callback=jQuery' + '211017959201466349473_' + str(timeStamp)

    erpapi_param = {
        'page':	'1',
        'pageSize':	'3',
        'user_type':	'1',
        'user_id':	'450',
        'unread':	'true'
    }
    Card_API = tools_request.post_Request(url_erpapi,erpapi_param,cookies = cookies)

    print('卡新建完毕___________[√]')


#------------------------------------------------------------------------------
#2016-08-03
#获取项目房间,这个方法暂时没啥用
def get_xkRoom(ipred,cookies):
    url = str(ipred) + 'admin.php?r=product/xkRoom/index&banid='+'116'
    building_house = tools_request.request_get(url,None,cookies=cookies)


# 通过项目id返回项目下的所有楼盘id
def sql_builing(brokerage_item_id,sql_connect):
    print('项目ID',brokerage_item_id)
    Array_building = tools_mysql.MysqlConnect("select building_id from building where item_id = "+str(brokerage_item_id),sql_connect)
    print ('所有楼盘id',Array_building)
    building_id = []
    for i in range(len(Array_building)):
        building_id.append(str(Array_building[i][0]))
    print ('返回项目下的所有楼盘id',building_id)
    return building_id

# 通过楼盘id 查询楼盘下的楼栋id号
def sql_xkban(building_id,sql_connect):
    Array_xk_ban_id = []

    for i in range(len(building_id)):
        Array_xk_ban_id.append(tools_mysql.MysqlConnect("select banid from erp_xk_ban where projectid = "+str(building_id[i]),sql_connect))
    # try:
    #     print('111')
    #     for i in range (len(building_id)):
    #         Array_xk_ban_id.append(tools_mysql.MysqlConnect("select banid from erp_xk_ban where projectid = "+str(building_id[i]),sql_connect)[0])
    # except Exception:
    #     print('222')
    #     for i in range (len(building_id)):
    #         Array_xk_ban_id.append(tools_mysql.MysqlConnect("select banid from erp_xk_ban where projectid = "+str(building_id[i]),sql_connect))
    print ('所有楼栋',Array_xk_ban_id)
    temp_xk_ban_id = []
    if len(Array_xk_ban_id)> 0:
        for i in range(len(Array_xk_ban_id)):
            for j in range(len(Array_xk_ban_id[i])):
                if(Array_xk_ban_id[i][j]):
                    temp_xk_ban_id.append(Array_xk_ban_id[i][j])

    type_xk_ban_id = [] # 用于将元组内容转换成list
    if len(temp_xk_ban_id) > 0 :
        if temp_xk_ban_id != None:
            if isinstance(temp_xk_ban_id[0],(tuple)):
                for i in range(len(temp_xk_ban_id)):
                    for j in range(len(temp_xk_ban_id[i])):
                        type_xk_ban_id.append(str(temp_xk_ban_id[i][j]))

    if type_xk_ban_id == None:
        print ('返回的楼栋id号',temp_xk_ban_id)
        return temp_xk_ban_id
    else:
        print ('返回的楼栋id号',type_xk_ban_id)
        return type_xk_ban_id


# 删除项目
def delete_brokeragetem(ipred,cookies,item_id):
    print('删除项目',item_id)
    url = str(ipred)+'/admin.php?r=product/brokeragetem/delete2&id='+str(item_id)
    delete_item = tools_request.request_get(url,None,cookies=cookies)


# 删除楼盘
def delete_building_get(ipred,cookies,building_id):
    print('删除楼盘',building_id)
    for i in range (len(building_id)):
        url = str(ipred) + 'admin.php?r=product/building/delete2&id='+str(building_id[i])
        tools_request.request_get(url,None,cookies=cookies)

# 删除楼栋
def delete_buildinghouse_get(ipred,cookies,xk_ban_id):
    tempArray = []
    print ('要删除的楼栋',xk_ban_id)
    for i in range(len(xk_ban_id)):
        if (xk_ban_id[i]):
            tempArray.append (str(xk_ban_id[i]))

    for i in range (len(tempArray)):
        url= str(ipred) + 'admin.php?r=product/XkBan/delete2&id='+str(tempArray[i])
        tools_request.request_get(url,None,cookies=cookies)

# 删除户型（房间）
def delete_buildinghouse_sql(building_id,sql_connect):
    building_house = []
    for i in range (len(building_id)):
        building_house.append(tools_mysql.MysqlConnect("select house_id FROM building_house WHERE building_id = "+building_id[i],sql_connect))
    for i in range(len(building_house)):
        print('楼盘：',building_id[i],'要删除的户型包括：',building_house[i])

    for i in range(len(building_id)):
        delete_buildinghouse = tools_mysql.MysqlConnect("DELETE FROM building_house WHERE building_id = "+str(building_id[i]),sql_connect)
        # print (delete_buildinghouse)

### 项目查询
def Brokeragetem_index(ipred,cookies,item_name,item_id):
    url = str(ipred) + 'admin.php?r=product/Brokeragetem/index&Brokeragetem[item_name]='+str(item_name)

    # item_id = tools_mysql.MysqlConnect('select item_id From brokerage_item where item_name ='+'"'+str(item_name)+'"',sql_connect)[0][0]
    Content = tools_request.request_get(url,None,cookies=cookies)
    soup = bs4.BeautifulSoup(Content,'html.parser')

    all_list_a = soup.find_all('table')
    re_item_name = re.findall(r'admin.php\?r=product/brokeragetem/view&amp;id='+str(item_id),str(all_list_a))
    if len(re_item_name) == 0:
        print('要查询的楼盘( '+ item_name + ' ) , 楼盘id： ('+ str(item_id) +' )不存在')
    else:
        print('查询到楼盘( '+ item_name + ' ) , 楼盘id： ('+ str(item_id) +' )')

# 通过数据库查询返回楼盘ID
def sql_getbuliding_id(building_name,sql_connect):
    try:
        buildingId =  tools_mysql.MysqlConnect('select building_id from building where building_name ='+'"'+str(building_name)+'"',sql_connect)[0][0]
    except:
        print("返回楼盘ID有错")
        return None

    return buildingId

def createBuiding(ipblue,ipred,item_code,item_name,sqlMysql):
    estateAgent_cookies = User_login.estateAgentlogin(ipblue)
    Admin_cookies = User_login.admin_login_blue(ipred)
    Brokeragetem,item_id = Brokeragetem_create(ip_red,Admin_cookies,item_code,item_name,sqlMysql)
    building_name = building_mysave(ipblue,estateAgent_cookies,item_id)                     # 创建楼盘，返回楼盘名称
    building_id = get_building_myowen(ipblue,estateAgent_cookies,building_name)             # 获取楼盘ID
    room_card_typeid = roomCardType(ipred,item_id,Admin_cookies,sqlMysql)                   # 新建卡类型
    createCardSave(ipred,Admin_cookies,item_code,room_card_typeid)                                # 新建卡

    return item_id

def delBuilding(ipblue,ipred,item_id,sqlMysql):
    admin_cookies = User_login.admin_login_blue(ipred)
    brokerage_item_id = item_id
    building_id = sql_builing(brokerage_item_id,sqlMysql)# 通过项目id返回楼盘id
    xk_ban_id = sql_xkban(building_id,sqlMysql)# 通过楼盘id 查询楼盘下的楼栋id号
    delete_buildinghouse_sql(building_id,sqlMysql)# 删除户型（房间）
    delete_buildinghouse_get(ipred,admin_cookies,xk_ban_id) # 删除楼栋
    delete_building_get(ipred,admin_cookies,building_id) # 删除楼盘
    delete_brokeragetem(ipred,admin_cookies,brokerage_item_id) # 删除项目
    Brokeragetem_index(ipred,admin_cookies,'python',brokerage_item_id)

def sql_getBuilid_IdAndName(sql_connect):
    message = tools_mysql.MysqlConnect('select building_id ,building_name from building',sql_connect)
    building_id = []
    building_name = []
    for i in range (len(message)):
        for j in range (len(message[i])):
            if j%2==1:
                building_name.append(message[i][j])
            else:
                building_id.append(message[i][j])

    return building_id,building_name

if __name__ == '__main__':
    print('-----')

    ip = Config.Ip()
    sqlconnect = Config.SqlConnect()

    # ip.set_Ipblue('http://test1www.xqshijie.com/')
    # ip.set_Ipred('http://test2www.xqshijie.com/')
    # sqlMysql = sqlconnect.get_fangfull_test_sql()



    ip.set_Ipblue('http://betawww.fangfull.com/')
    ip.set_Ipred('http://betaerp.fangfull.com/')
    sqlMysql = sqlconnect.get_fangfull_beta_sql()


    ip_blue = ip.get_Ipblue()
    ip_red = ip.get_Ipred()


    item_code  = '13'
    # item_name = '
    # '
    # ## 创建
    # item_id = createBuiding(ip_blue,ip_red,item_code,item_name,sqlMysql)
    # print('=================')
    ## 删除

    # item_code = [123,6,8,14,23]
    # for i in range(len(item_code)):
    #     delBuilding(ip_blue,ip_red,str(item_code[i]),sqlMysql)

    # print('item_id === ',item_id)


    # item_id = ['100']
    # delBuilding(ip_blue,ip_red,item_id,sqlMysql)


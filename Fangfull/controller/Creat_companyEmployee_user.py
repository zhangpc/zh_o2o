# -*- coding:utf-8 -*-
#!/usr/bin/python

from Fangfull.controller import User_login,Building
import tools_request
import tools_mysql
from config import Config

# sql_connect = Config.sql_connect(Config.sql_index).set_connect()
# 创建erp用户（内部用户）返回内部用户ID 和 名称
# Department_name（部门）
# CompanyEmployee_role_name（角色名称）
# CompanyEmployee_name （自定义的员工名称）
# CompanyEmployee_username （自定义登录账户）
#返回创建成功后的角色名称和ID
def create_CompanyEmployee(ipred,cookies,Department_name,CompanyEmployee_role_name,CompanyEmployee_name,CompanyEmployee_username,sql_connect):
    url = str(ipred) + 'admin.php?r=product/companyEmployee/create'
    #获取角色ID
    sql_CompanyEmployeeRole_id = tools_mysql.MysqlConnect('select id from erp_company_employee_role where name = '+'"'+str(CompanyEmployee_role_name)+'"',sql_connect)[0][0]


    sql_Department_id = tools_mysql.MysqlConnect('select id from erp_department where depart_name = '+str(Department_name),sql_connect)

    params = {
        'CompanyEmployee[name]':str(CompanyEmployee_name),
        'CompanyEmployee[sex]':'1',
        'CompanyEmployee[superior]':'0',#上级员工，应该是个网格经理
        'CompanyEmployee[company_id]':'2',##员工所属公司
        'CompanyEmployee[depart_id]':str(sql_Department_id),## 员工所属部门（华北大区）
        'CompanyEmployee[username]':str(CompanyEmployee_username),
        'CompanyEmployee[password]':'654321',
        'CompanyEmployee[title]':str(CompanyEmployee_name),
        'CompanyEmployee[mobile]':'13600000001',
        'CompanyEmployee[email]':'ztx1501@sina.com',
        'CompanyEmployee[status]':'1',
        'CompanyEmployeeRole[id]':str(sql_CompanyEmployeeRole_id),#项目总监  #案场讲解员4
    }
    creat_xmzj = tools_request.post_Request(url,params,cookies=cookies)
    employee_id,employee_name=tools_mysql.MysqlConnect('select id,name from erp_company_employee where username = '+'"'+str(CompanyEmployee_username)+'"',sql_connect)[0]
    print("角色名称："+str(sql_CompanyEmployeeRole_id),"自定义名称："+str(CompanyEmployee_username),"创建成功后的角色ID"+str(employee_id),"创建成功后的角色名称"+str(employee_name))
    return employee_id,employee_name

## 分配案场，传递erp用户ID 名称 和楼盘名称
def addBuilding(ipred,cookies,employee_id,employee_name,building_name,sql_connect):
    url = str(ipred) + 'admin.php?r=product/mgr/AddBuilding'
    buildingId =  tools_mysql.MysqlConnect('select building_id from building where building_name ='+'"'+str(building_name)+'"',sql_connect)[0][0]
    params={
        'employee_name':str(employee_name),
        'employee_id':str(employee_id),
        'building_id':str(buildingId),
        'company_name[]':str(building_name),
        'sub':'分配',
    }
    addBuilding = tools_request.post_Request(url,params,cookies=cookies)
def sql_getEmployeeId(Employee_Name,sql_connect):
    employee_id,employee_name = tools_mysql.MysqlConnect('select id,name from erp_company_employee where username ='+'"'+str(Employee_Name)+'"',sql_connect)[0]

    return employee_id,employee_name
# 开始新建
def Creat_implement():
    # ip = Config.Ip()
    # ip.set_Ipblue('http://test15www.xqshijie.com/')
    # ip.set_Ipred('http://test16www.xqshijie.com/')
    # ip_blue = ip.get_Ipblue()
    # ip_red = ip.get_Ipred()
    # sqlconnect = Config.SqlConnect()
    # sqlMysql = sqlconnect.get_fangfull_test_sql()



    ip = Config.Ip()
    ip.set_Ipblue('http://betawww.fangfull.com/')
    ip.set_Ipred('http://betaerp.fangfull.com/')
    ip_blue = ip.get_Ipblue()
    ip_red = ip.get_Ipred()
    sqlconnect = Config.SqlConnect()
    sqlMysql = sqlconnect.get_fangfull_beta_sql()


    Department_name = '华北区案场部'#东北区案场部   #华北区案场部 #销售中心
    Building_name='北京中弘大厦' #北京中弘大厦 #新奇世界-半山半岛 # 新奇世界-夏各庄由山由谷
    CompanyEmployee_role_name = ['项目总监','案场讲解员','案场订单录入','案场后台客服','总部财务','案场财务','经纪公司结佣信息审核员','计划部网签审核','渠道佣金审核']
    CompanyEmployee_name = ['z测试项目总监','z测试案场讲解员','z测试案场订单录入员','z测试案场后台客服','z测试总部财务','z测试案场财务','z测试经纪公司结佣信息审核员','z计划部网签审核','z渠道佣金审核']
    CompanyEmployee_username=['zcsxmzj','zcsacjjy','zcsacddlry','zcsachtkf','zcszbcw','zcsaccw','zcsjyshy','zcsjhbwq','zcsqdyjsh']

    # CompanyEmployee_role_name = ['计划部网签审核','渠道佣金审核']
    # CompanyEmployee_name = ['z计划部网签审核','z渠道佣金审核']
    # CompanyEmployee_username=['zcsjhbwq','zcsqdyjsh']


    admin_cookies = User_login.admin_login_blue(ip_red)

    #创建erp用户（内部用户）返回内部用户ID 和 名称
    for i in range(len(CompanyEmployee_role_name)):
        employee_id,employee_name = create_CompanyEmployee(ip_red,admin_cookies,Department_name,
                                                           CompanyEmployee_role_name[i],
                                                           CompanyEmployee_name[i],
                                                           CompanyEmployee_username[i],
                                                           sqlMysql
                                                           )
        if i <= 6:
            addBuilding(ip_red,admin_cookies,employee_id,employee_name,Building_name,sqlMysql)

if __name__ == '__main__':
    # Creat_implement()


    # ip = Config.Ip()
    # ip.set_Ipblue('http://test1www.xqshijie.com/')
    # ip.set_Ipred('http://test2www.xqshijie.com/')
    # ip_blue = ip.get_Ipblue()
    # ip_red = ip.get_Ipred()
    # sqlconnect = Config.SqlConnect()
    # sqlMysql = sqlconnect.get_fangfull_test_sql()
    # building_id,building_name = Building.sql_getBuilid_IdAndName(sqlMysql)
    # for i in range(len(building_id)):
    #     print(building_id[i],building_name[i])

    #
    ip = Config.Ip()
    ip.set_Ipblue('http://betawww.fangfull.com/')
    ip.set_Ipred('http://betaerp.fangfull.com/')
    ip_blue = ip.get_Ipblue()
    ip_red = ip.get_Ipred()
    sqlconnect = Config.SqlConnect()
    sqlMysql = sqlconnect.get_fangfull_beta_sql()


    # ip = Config.Ip()
    # ip.set_Ipblue('http://test1www.xqshijie.com/')
    # ip.set_Ipred('http://test2www.xqshijie.com/')
    # ip_blue = ip.get_Ipblue()
    # ip_red = ip.get_Ipred()
    # sqlconnect = Config.SqlConnect()
    # sqlMysql = sqlconnect.get_fangfull_test_sql()
    #
    #
    employee_user_name = 'zcsaccw'
    Building_name = '新奇世界-半岛蓝湾'#'济南中弘广场' #'北京中弘大厦' #新奇世界-夏各庄由山由谷 #新奇世界-半山半岛 #新奇世界-济南鹊山 #新奇世界-半岛蓝湾
    employee_id,employee_name = sql_getEmployeeId(employee_user_name,sqlMysql)
    admin_cookies = User_login.admin_login_blue(ip_red)
    addBuilding(ip_red,admin_cookies,employee_id,employee_name,Building_name,sqlMysql)











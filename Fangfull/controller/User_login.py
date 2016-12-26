# -*- coding:utf-8 -*-
#!/usr/bin/python
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
import tools_request
from config import Config


#管理员用户登录蓝色后台
def admin_login_blue(ipred):
    parameter = {
        'LoginForm[username]': 'admin',
        'LoginForm[password]': '654321'
    }

    print('admin登录==',str(ipred))
    url = str(ipred)+'admin.php?r=product/default/login'
    Admin_cookies,Content = tools_request.get_Userlogin_cookies(url,parameter,None)
    return Admin_cookies

#管理员用户登录红色后台
def admin_login_red(ipred):
    parameter = {
        'LoginForm[username]': 'admin',
        'LoginForm[password]': '654321'
    }
    admin_url = str(ipred)+'admin.php?r=product/default/login'
    Admin_cookies,red_url = tools_request.get_Userlogin_cookies(admin_url,parameter,None)
    if Admin_cookies != None and red_url != None:
        red_cookies = tools_request.get_request_cookies(red_url,cookies=Admin_cookies)
        return red_cookies
    return None
#经纪公司管理员登陆
def broker_companylogin(ipblue,login_name):
    url = str(ipblue)+'admin/brokerCompanyLogin'
    parameter={
        'LoginForm[username]':str(login_name),#testhb_001_001 testhb_007_005,testhb_007_007
        'LoginForm[password]':'123456',
        }
    brokerCompany_cookies,Content = tools_request.post_Request(url,parameter)

    return brokerCompany_cookies
#经纪人登录
def broker_login(ipblue,username):

    url = str(ipblue)+"admin/brokerLogin"
    parameter={
        'LoginForm[username]':username,#testhb_001_001 testhb_007_005,testhb_007_007
        'LoginForm[password]':'123456',
        }
    broker_cookies,Content = tools_request.post_Request(url,parameter)
    print (tools_request.Assert('欢迎您',Content,1))
    # print broker_cookies
    # print Content
    return broker_cookies


# 案场讲解员登录_blue
def acgly_login_blue(ipblue,username):
    url = str(ipblue)+"admin.php?r=product/default/login"
    parameter = {
        'LoginForm[username]':str(username),#adhce_acjjy
        'LoginForm[password]':'654321',
    }
    acgly_cookies,red_url = tools_request.get_Userlogin_cookies(url,parameter,None)
    print("登录",username,"返回cookies")
    return acgly_cookies

# 案场讲解员登录_red
def acgly_login_red(ipred,username):
    url = str(ipred)+"admin.php?r=product/default/login"
    parameter = {
        'LoginForm[username]':str(username),#acjjy_bjzhgc,csacjjy
        'LoginForm[password]':'654321',
    }
    acgly_cookies,red_url = tools_request.get_Userlogin_cookies(url,parameter,None)
    red_cookies = tools_request.get_request_cookies(red_url,cookies=acgly_cookies)
    return red_cookies

# 案场客服登录蓝色页面
def ackf_login_blue(ipred,username):
    url = str(ipred)+"admin.php?r=product/default/login"
    parameter = {
        'LoginForm[username]':str(username),#ackf_bjzhgc #csachtkf
        'LoginForm[password]':'654321',
    }
    ackf_cookies,red_url = tools_request.get_Userlogin_cookies(url,parameter,None)

    return ackf_cookies

# 案场客服登录红色页面
def ackf_login_red(ipred):
    url = str(ipred)+"admin.php?r=product/default/login"
    parameter = {
        'LoginForm[username]':'zcsachtkf',#ackf_bjzhgc #csachtkf
        'LoginForm[password]':'654321',
    }
    ackf_cookies,red_url = tools_request.get_Userlogin_cookies(url,parameter,None)
    red_cookies = tools_request.get_request_cookies(red_url,cookies=ackf_cookies)
    return red_cookies

#案场订单录入员直接登录红色后台（他没有蓝色后台）
def acddlry_login_red(ipred):
    url = str(ipred)+"admin.php?r=product/default/login"
    parameter = {
        'LoginForm[username]':'zcsacddlry',
        'LoginForm[password]':'654321',
    }
    acddlry_cookies = tools_request.get_Userlogin_cookies_red(url,parameter,None)[0]
    return acddlry_cookies

#案场财务登录红色后台
def accw_login_red(ipred):
    url = str(ipred)+"admin.php?r=product/default/login"
    parameter = {
        'LoginForm[username]':'zcsacddlry',
        'LoginForm[password]':'654321',
    }
    accw_cookies = tools_request.get_Userlogin_cookies_red(url,parameter,None)[0]
    return accw_cookies


##总部财务登录蓝色后台
def zbcw_login_blue(ipred):
    url = str(ipred)+"admin.php?r=product/default/login"
    parameter = {
        'LoginForm[username]':'zcszbcw',
        'LoginForm[password]':'654321',
    }
    ackf_cookies,red_url = tools_request.get_Userlogin_cookies(url,parameter,None)
    return ackf_cookies

#总部财务登录红色后台
def zbcw_login_red(ipred):
    url = str(ipred)+"admin.php?r=product/default/login"
    parameter = {
        'LoginForm[username]':'zcszbcw',
        'LoginForm[password]':'654321',
    }
    # zbcw_cookies = request.get_Userlogin_cookies_red(url,parameter,None)
    zbcw_cookies,red_url = tools_request.get_Userlogin_cookies(url,parameter,None)
    zbcw_red_cookies = tools_request.get_request_cookies(red_url,cookies=zbcw_cookies)
    return zbcw_red_cookies

#项目总监登录蓝色后台
def xmzj_login_blue(ipred,username):
    url = str(ipred)+"admin.php?r=product/default/login"
    parameter = {
        'LoginForm[username]':str(username),
        'LoginForm[password]':'654321',
    }
    ackf_cookies,red_url = tools_request.get_Userlogin_cookies(url,parameter,None)
    return ackf_cookies

#项目登录红色后台
def xmzj_login_red(ipred,username):
    parameter = {
        'LoginForm[username]': str(username),
        'LoginForm[password]': '654321'
    }
    admin_url = str(ipred)+'admin.php?r=product/default/login'
    Admin_cookies,red_url = tools_request.get_Userlogin_cookies(admin_url,parameter,None)
    if Admin_cookies != None and red_url != None:
        red_cookies = tools_request.get_request_cookies(red_url,cookies=Admin_cookies)
        return red_cookies
    return None

# 开发商登录
def estateAgentlogin(ipblue):
    url = str(ipblue) + "admin/estateAgentlogin"
    parameter = {
        'LoginForm[username]':'python_beta',
        'LoginForm[password]':'12345678',
    }
    estateAgent_cookies = tools_request.get_Userlogin_cookies_red(url,parameter,None)[0]
    return estateAgent_cookies
if __name__ == "__main__":
    ipset = Config.Ip()
    ipset.set_Ipblue('http://test1www.xqshijie.com/')
    ipset.set_Ipred('http://test2www.xqshijie.com/')

    admin_login_red(ipset.get_Ipred())
    # broker_login()
    # cookies = acgly_login_red()

    # ackf_login_blue()
    # print ackf_login_red()
    # acddlry_cookies = acddlry_login_red()
    # accw_cookies = accw_login_red()
    # print accw_cookies

    # zbcw_cookis = zbcw_login_red()
    # print zbcw_cookis

    # print (xmzj_login_blue())

    # print(ipset.get_Ipblue())
    # print(ipset.get_Ipred())
    # estateAgent_cookies = estateAgentlogin(ipset.get_Ipblue())
    # print (estateAgent_cookies)

    xmzj_cookies = xmzj_login_blue('http://test2www.xqshijie.com/','zcsxmzj')
    print(xmzj_cookies)

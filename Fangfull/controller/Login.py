# -*- coding:utf-8 -*-
__author__ = 'Administrator'
import  sys
from poster.streaminghttp import register_openers

import cookielib
import requests
import urllib2
import urllib
# from Request.common import request

# global browser_heard
browser_heard = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
                 'Connection': 'keep-alive',
                 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                 'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                 }

def getCookies_Dict(cookies):
    keys = []
    values = []

    for item in cookies:
        keys.append(item.name)
        values.append(item.value)
        # print (str(keys[item]) + "  " + str(values[item]))
    # print ('55555555555555555555')
    # print (dict(zip(keys,values)))
    cookies = dict(zip(keys,values))

    return cookies

def admin_login():
    parameter = {
        'LoginForm[username]': 'admin',
        'LoginForm[password]': '123456'
    }
    url = 'http://testwww.xqshijie.com/xqsjadmin.php?r=site/login'


    data = urllib.urlencode(parameter)
    cookie = cookielib.CookieJar()
    handler=urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    response = opener.open(url,data)
    content = response.read()
    return getCookies_Dict(cookie)


    # getcookies =requests.post(url,parameter,headers = browser_heard)
    # print (getcookies.cookies)
    # print(getcookies.text)


    # req_session = requests.session()
    # response = req_session.post(url,params = parameter,headers = browser_heard)
    # getcookies = getCookies_Dict(response.cookies)
    # print(req_session.cookies)
    # print (response.cookies)
    # print(response.text)

    # return getcookies


def get_welcome(cookies):
    url = 'http://testwww.xqshijie.com/xqsjadmin.php?r=site/welcome'
    # # print (cookies)
    # # rr = requests.get(url)
    # # # print (rr.cookies)
    # # return rr.cookies
    # req_session = requests.session()
    # response = req_session.get(url,cookies=cookies,headers=browser_heard)
    # # print (cookies)
    # # print (response.headers)
    # print (response.text)
    # dict_cookies = getCookies_Dict(response.cookies)
    # return dict_cookies

    # data = urllib.urlencode(parameter)
    # cookie = cookielib.CookieJar()

    handler=urllib2.HTTPCookieProcessor(cookies)
    opener = urllib2.build_opener(handler)
    response = opener.open(url)

    content = response.read()
    # print handler.cookiejar
    # return getCookies_Dict(cookie)


def get_project(cookies):
    parameter = {
                'r':'project/index',
                'project[project_name]': '测试',
                 'project[ff_item]': '',
                 'project[last_modified]': '',
                 'project[last_modifieds]': '',
                 'project[create_username]': '',
                 'project[project_status]': '2',
                 }

    url = 'http://testwww.xqshijie.com/xqsjadmin.php?project/index'

    req_session = requests.session()
    response = req_session.post(url,params = parameter,cookies=cookies,headers = browser_heard)

    print (response.text)


if __name__ == '__main__':
    cookies = admin_login()
    get_project(cookies)


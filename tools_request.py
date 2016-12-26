# -*- coding:utf-8 -*-
#!/usr/bin/python
import json
import urllib
import requests

# import cookielib
import http.cookiejar
import re
from urllib3.filepost import encode_multipart_formdata
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pprint
#from poster.encode import multipart_encode
# from poster.streaminghttp import register_openers
# import  sys
# from imp import reload
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
# register_openers()



global browser_heard
browser_heard = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
                 'Connection': 'keep-alive',
                 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                 'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                 }

def set_strSplit(dictText):
    index = 1
    text = ""
    for i in dictText:
        if i != "{":
            text = dictText[index:]
            index = index+1
        else:
            break
    return text

## 浏览器 Post 请求
def post_Request(url,data,**kwargs):

    if data != None:
        if len(kwargs.keys()) > 0:
            if kwargs['cookies'] != None:
                # print (kwargs['cookies'])
                # print ("带参数，带cookies的post请求")
                try:
                    response = requests.post(str(url),data = data,cookies=kwargs['cookies'],headers=browser_heard)
                    # print(response.text)
                    return response.text
                except IOError as e:
                    print(e)
                    return None

                # print response.text

        else:
            # print ("带参数，不带cookies的post请求")
            req_session = requests.session()
            try:
                response = req_session.post(str(url),data = data,headers=browser_heard)
                cookies = getCookies_Dict(req_session.cookies)
                return cookies,response.text
            except IOError as e:
                print(e)
                return None
    else :
        # print("不带参数，带cookies的post")
        if len(kwargs.keys()) > 0:
            if kwargs['cookies'] != None:
                try:
                    response = requests.post(str(url),cookies=kwargs['cookies'],headers=browser_heard)
                    return response.text
                except IOError as e:
                    print(e)
                    return None
        # print (response.cookies)
        # print (response.text)


# ## 浏览器 Get 请求
# def Resquest_get(url,**kwargs):
#     rqe = requests.get(url,headers=browser_heard)
#     print (rqe.cookies)
#     print (rqe.text)

## 获取用户 Cookies
def get_Userlogin_cookies(url,data,cookie):
    # data = urlencode(data).encode()
    if cookie == None:
        cookie = http.cookiejar.CookieJar()
    import traceback
    handler=urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    istry = True
    try:
        response = opener.open(url,urllib.parse.urlencode(data).encode())
    except IOError as e:
        istry = False
        print(e)
        return None
    if istry:
        content = response.read()
        content_decode = content.decode()
        # print(content_decode)
        soup = BeautifulSoup(content_decode, 'html.parser')

        # print(soup.title,type(str(soup.title)))
        if "登录" not in str(soup.title):

            textA_all_list = soup.body.find_all('a')
            textA_all_str = ''.join(str(textA_all_list))
            url_Red = re.findall(r'href="(http\:\/\/.*?token\/.*)">',str(textA_all_str))
            keys = []
            values = []
            for item in cookie:
                keys.append(item.name)
                values.append(item.value)
            cookies = dict(zip(keys,values))
            # print (response.read())
            # for item in cookie:
            #     print ('Name = '+item.name)
            #     print ('Value = '+item.value)
            # print (url_Red[0])
            return cookies,url_Red[0]
        else:
            print("登录失败:",data)
            return None,None
    else:
        return None,None


# 直接登录红色界面
def get_Userlogin_cookies_red(url,data,cookie):
    # data = urlencode(data)
    # print (data)
    if cookie == None:
        cookie = http.cookiejar.CookieJar()
    try:
        handler=urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)
        response = opener.open(url,urllib.parse.urlencode(data).encode())
        content = response.read()
    except IOError as e:
        return None
    content_decode = content.decode()
    # print (content_decode)
    keys = []
    values = []
    cookies = []
    for item in cookie:
        keys.append(item.name)
        values.append(item.value)
        cookies.append(dict(zip(keys,values)))

    return cookies

## 普通get方法
def get_request_cookies(url,cookies):
    if cookies == None:
        try:
            response = requests.get(url)
        except IOError as e:
            print(e)
            return None

        return response.text
    else:
        req_session = requests.session()
        try:
            response = req_session.get(str(url),headers=browser_heard)
            getcookies = getCookies_Dict(req_session.cookies)
        except IOError as e:
            print(e)
            return None



        # print (response.text)
        # s = requests.Session()
        # s.get(url)
        # c = s.cookies
        # cookie = getCookies_Dict(s.cookies)
        return getcookies

def request_get(url,params,**kwargs):
    try:
        response = requests.get(str(url),data=params,headers=browser_heard,cookies=kwargs['cookies'])
    except IOError as e:
        print(e)
        return None
    return response.text


def Resquest_post(url,data):
    try:
        r = requests.post(str(url),data)
    except IOError as e:
        print(e)
        return None
    return r

def Resquest_poster(url,body):
    body,headers = encode_multipart_formdata(body)
    request = urllib.request(url,body,headers=browser_heard)
    response = urllib.urlopen(request).read()
    res = set_strSplit(response)
    Dict_Json = get_DictJson(res)
    return Dict_Json

def get_DictJson(str_Json):
    # text = json.loads(str_Json)
    # dictJson = json.dumps(text,ensure_ascii=False)
    # dictJson = eval(dictJson)
    dictJson = json.loads(str_Json,encoding='utf-8')
    return dictJson



def Request_getApp(url):
    re = requests.get(str(url),verify=False)
    return re

# def request_get(url,params,**kwargs):
#
#     response = requests.get(str(url),data=params,headers=browser_heard,cookies=kwargs['cookies'])
#     # print (response.text)


    return response.text

def Request_postApp(url,data):
    # r = requests.post(url,params=data ,verify = False)
    # print (r.json())
    # if 'result' in r.json():
    #     print ('sdfsdfsdf')
    try:
        r = requests.post(url,params=data ,verify = False)
        if r.status_code == 200 and r.json() != None:
            return r.json()
    except Exception as e:
        print (e,'接口调用出现异常')
        return

# 结果值断言
def Assert(var1 ,var2,type,**kwargs):
    key = [key for key in kwargs ]

    if 'describe' in key :
        if type == 0:
            try:
                assert var1 == var2
                print ("断言结果正确，" + "期望结果：" + str(var1) + " 与实际值一致",kwargs['describe'])
                return True
            except:
                print ("结果不匹配："+"期望值 "+str(var1)+" 与实际值不一致",kwargs['describe'])
                return False
        elif type == 1:
            try:
                assert var1 in var2
                print ("断言结果正确，" + "期望结果：" + str(var1) + " 在实际结果中",kwargs['describe'])
                return True
            except:
                print ("结果不匹配："+"期望值 "+str(var1)+" 与实际值不一致",kwargs['describe'])
                return False


    else:
        if type == 0:
            try:
                assert var1 == var2
                # print ("断言结果正确，" + "期望结果：" + str(var1) + " 与实际值一致")
                return True
            except:
                # print ("结果不匹配："+"期望值 "+str(var1)+" 不实际值不一致")
                return False
        elif type == 1:
            try:
                assert var1 in var2
                # print ("断言结果正确，" + "期望结果：" + str(var1) + " 在实际结果中")
                return True
            except:
                # print ("结果不匹配："+"期望值 "+str(var1)+" 不在实际值中")
                return False


#浏览器获取的cookies 转换成字典格式
def getCookies_Dict(cookies):
    keys = []
    values = []
    for item in cookies:
        keys.append(item.name)
        values.append(item.value)
    cookies = dict(zip(keys,values))
    return cookies

def re_return_message(html):
    css = "<h5 style='color:orangered;font-size:25px; padding-top:20px;' [^?]([\w\W]+)</h5>"
    message = re.findall(css,html)[0]
    return message

# def tools_BeautifulSoup(content,Label):
#     soup = BeautifulSoup(content, 'html.parser')
#     textA_all_list = soup.body.find_all(Label)
#     return textA_all_list


def get_request(url):
    response = requests.get(url)
    return response

if __name__ == "__main__":
    print("3")
    # # 第一种方式 ：requests
    # Url = "qmjjrwap.php?r=site/loginAjax"
    # Data = {'phone':'13600000001','pwd':'123456'}
    # r = post_Request(Url,Data)
    # text = set_strSplit(r.text)
    # Dict_Json = get_DictJson(text)
    # print Dict_Json

    # 第二种方式：poster/urllib2
    # Url_login = "qmjjrwap.php?r=site/loginAjax"
    # # url = "http://testwww.xqshijie.com/qmjjrwap.php?r=site/loginAjax"
    # body = {'phone':'13600000001','pwd':'1234561'}
    # response = Resquest_poster(Url_login,body=body)
    # print response

    # Url_getVeriCode = "qmjjrwap.php?r=site/getVeriCode"
    # body = {'phone':'13600000001'}
    # response = Resquest_poster(Url_getVeriCode,body=body)
    # print response
    # print str(Config_request.IP)

    # # get
    # url = "http://192.168.9.168/check/571ee23d1437b52dc0beef77"
    # body = {'phone':'13600000001','pwd':'1234561'}
    # get = Resquest_get(url,body=body)
    # print get

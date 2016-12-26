# -*- coding:utf-8 -*-
#!/usr/bin/python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os
from config import Config
from QuanminJingjiren.static import img
from urllib import parse
from selenium.webdriver.support.select import Select
from Fangfull.controller import User_login,Broker_company,Broker

class Selenium():
    def loading_Firefox(self):
        self.browser = webdriver.Firefox() # Get local session of firefox
    def open_url(self,url,sleep):
        self.browser.get(url) # Load page
        time.sleep(sleep)
    def close_browser(self,sleep):
        time.sleep(sleep)
        self.browser.close()
    def get_id(self,id,sleep):
        time.sleep(sleep)
        by_element = None
        try:
            by_element = self.browser.find_element_by_id(id)
            if by_element.is_displayed():
                return by_element
            else:
                print("没有定位到元素：",id)
                return None
        except:
            print("没有定位到元素：",id)
            self.browser.stop_client()
            return None


    def get_tagName(self,tagName,sleep):
        time.sleep(sleep)
        by_element = None
        try:
            by_element = self.browser.find_element_by_id(tagName)
            if by_element.is_displayed():
                self.get_message_ok('tagName',tagName)
                return by_element
        except:
            self.get_message_error('tagName',tagName)
            self.browser.stop_client()
            return None

    def get_xpath(self,xpath,sleep):

        by_element = None
        try:
            time.sleep(sleep)
            by_element = self.browser.find_element_by_xpath(xpath)
            if by_element.is_displayed():
                self.get_message_ok('xpath',xpath)
                return by_element
        except:
            self.get_message_error('xpath',xpath)
            self.browser.stop_client()
            return None

    def get_className(self,className,sleep):
        time.sleep(sleep)
        by_element = None
        try:
            by_element = self.browser.find_element_by_class_name(className)
            if by_element.is_displayed():
                return by_element
            else:
                print("没有定位到元素：",className)

        except:
            print("异常错误，检查在定位：" + className)
            self.browser.stop_client()
            return None

    def send_key(self,element,value,sleep):
        if element!=None:
            time.sleep(sleep)
            try :
                element.clear()
                element.send_keys(value)
                return True
            except:
                print('send_key 写入出错')
                return None
        else:
            self.browser.stop_client()
            return None

    #下拉菜单单选
    def select_options(self,element,value,sleep):
        time.sleep(sleep)
        if element != None:
            Select(element).select_by_value(value)
            return True
        else:
            self.browser.stop_client()
            return False

    def on_click(self,element,sleep):

        if element!=None:
            time.sleep(sleep)
            try:
                element.click()
                print('点击成功')
                return True
            except:
                print("点击事件失败")
                return False
        else:
            print('点击失败')
            self.browser.stop_client()
            return False

    def current_window_handle(self):
        now_handle = self.browser.current_window_handle #得到当前窗口句柄
        print (now_handle.title)
        return now_handle
    def max_window(self):
        self.browser.maximize_window()
    #获取当前浏览器的地址
    def get_url(self):
        return self.browser.current_url

    def get_message_ok(self,type,elements):
        print (type+'定位元素成功：',elements)
    def get_message_error(self,type,elements):
        print("使用"+type+"未定位到元素:",elements)
    # 没用到
    # def tryExcept(self,find_element,element):
    #     try:
    #         if find_element.is_displayed():
    #
    #             return find_element
    #         else:
    #             print("没有定位到元素：",element)
    #             return None
    #     except :
    #         print("异常错误，检查在定位：" + element)



if __name__ == '__main__':
    #
    print('运行前置脚本')
    broker_compary_name = '自动化测试12'
    broker_compary_phone = '13680001012'
    admin_cookies = User_login.admin_login_red()
    broker_compary_id = Broker.creat_Broker_company(admin_cookies,broker_compary_name,broker_compary_phone) # 创建经纪公司
    broker_companyadmin_name = Broker.savebrokerCompanyAdmin(admin_cookies,broker_compary_id,broker_compary_phone) #创建经纪公司管理员
    brokerCompany_cookies = User_login.broker_companylogin(broker_companyadmin_name)#经纪公司管理员登陆
    Broker_company.Broker_mysave(brokerCompany_cookies,broker_compary_phone) #创建经纪人
    print('经纪公司管理员账号',broker_companyadmin_name)
    print('经纪人账号:',broker_compary_phone)

#
#     print('运行自动化')
#     Selenium = Selenium()
#     Selenium.loading_Firefox()
#     # Selenium.max_window()
#     open_quanminjingjiren  = Config_IP.IP_Jigoujingjiren
#     Selenium.open_url(open_quanminjingjiren,3)
#     input_phone = Selenium.get_id('phone',0)
#     Selenium.send_key(input_phone,str(broker_compary_phone),0)
#     input_password = Selenium.get_id('password',0)
#     Selenium.send_key(input_password,'123456',0)
#     btn_submit = Selenium.get_xpath('//a[contains(text(),"登录")]',0)
#     Selenium.on_click(btn_submit,0)
#
#
# ### 上传身份证
#     into_My_IDcard = Selenium.get_xpath('//ul/li[1]/a',2) #进入身份填写页面
#     Selenium.on_click(into_My_IDcard,0)
#     input_name_card = Selenium.get_id('name_on_card',0)
#     Selenium.send_key(input_name_card,'前端自动添加',0)
#     input_card_number = Selenium.get_id('card_number',0)
#     Selenium.send_key(input_card_number,'152801198703025310',0)
#
#     input_card_face = Selenium.get_xpath('//ul/li[3]/div/div[2]/div[2]/input',0)
#     Selenium.send_key(input_card_face,'E:\文档\svn文档\自动化\Myproject\QuanminJingjiren\static\img\card_face.png',2)
#
#     input_card_black = Selenium.get_xpath( '//ul/li[4]/div/div[2]/div[2]/input',0)
#     Selenium.send_key(input_card_black,'E:\文档\svn文档\自动化\Myproject\QuanminJingjiren\static\img\card_black.png',2)
#
#     btn_ok = Selenium.get_xpath('//button[contains(text(),"确定")]',0)
#     Selenium.on_click(btn_ok,2)
#
# ##### 上传银行卡
#     open_userinfo = Config_IP.IP_Jigoujingjiren+'?r=admin/userinfo'
#     Selenium.open_url(open_userinfo,1)
#
#     into_mybankcard = Selenium.get_xpath('//span[contains(text(),"我的银行卡")]',0)
#     Selenium.on_click(into_mybankcard,0)
#
#     input_card_holder_name = Selenium.get_id('card_holder_name',4)
#     Selenium.send_key(input_card_holder_name,'自动化测试',0)
#
#     input_select_card = Selenium.get_id('bank_id',0)
#     Selenium.select_options(input_select_card,'4',0)
#
#     input_card_number = Selenium.get_id('card_number',0)
#     Selenium.send_key(input_card_number,'6225000000000001',0)
#
#     input_bank_branch_name = Selenium.get_id('bank_branch_name',0)
#     Selenium.send_key(input_bank_branch_name,'自动化测试_支行名称',0)
#
#     input_bank_city = Selenium.get_id('bank_city',0)
#     Selenium.send_key(input_bank_city,'自动化测试_城市名称',0)
#
#     input_img_card = Selenium.get_xpath('//ul/li[7]//input',0)
#     Selenium.send_key(input_img_card,'E:\文档\svn文档\自动化\Myproject\QuanminJingjiren\static\img\card_blank.png',2)
#
#     btn_card = Selenium.get_xpath('//button[contains(text(),"确定")]',0)
#     Selenium.on_click(btn_card,2)


# ## 已结佣
#     open_userinfo = Config_IP.IP_Jigoujingjiren+'?r=admin/userinfo'
#     Selenium.open_url(open_userinfo,1)
#
#     btn_commissionHave = Selenium.get_xpath('//a[contains(text(),"已结佣")]',0)
#     Selenium.on_click(btn_commissionHave,0)
#
#
# ## 可结佣
#     open_userinfo = Config_IP.IP_Jigoujingjiren+'?r=admin/userinfo'
#     Selenium.open_url(open_userinfo,1)
#     btn_commissionCan = Selenium.get_xpath('//a[contains(text(),"可结佣")]',0)
#     Selenium.on_click(btn_commissionCan,0)
# #     //a[contains(text(),"可结佣")]












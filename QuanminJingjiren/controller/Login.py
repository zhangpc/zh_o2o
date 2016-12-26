from QuanminJingjiren.common import Selenium
from config import Config
from selenium.webdriver.support.select import Select
from Fangfull.controller import User_login,Broker_company,Broker
def quangminjinjiren(url_qm,broker_compary_phone,broker_name):
    selenium = Selenium.Selenium()
    selenium.loading_Firefox()
    # selenium.max_window()
    open_quanminjingjiren  = str(url_qm)+str(Config.IP_Quanminjingjiren)
    selenium.open_url(open_quanminjingjiren,3)

    btn_login_page = selenium.get_xpath('//footer//li/a[contains(text(),"我的")]',1)
    selenium.on_click(btn_login_page,0)
    input_phone = selenium.get_id('phone',0)
    selenium.send_key(input_phone,str(broker_compary_phone),0)
    input_password = selenium.get_id('password',0)
    selenium.send_key(input_password,'123456',0)
    btn_submit = selenium.get_xpath('//a[contains(text(),"登录")]',0)
    selenium.on_click(btn_submit,0)

### 上传身份证
    into_My_IDcard = selenium.get_xpath('//span[contains(text(),"我的身份证")]',3) #进入身份填写页面
    selenium.on_click(into_My_IDcard,1)
    input_name_card = selenium.get_id('name_on_card',0)
    selenium.send_key(input_name_card,str(broker_name),0)
    input_card_number = selenium.get_id('card_number',0)
    selenium.send_key(input_card_number,'152801198703025310',0)

    input_card_face = selenium.get_xpath('//ul/li[3]/div/div[2]/div[2]/input',0)
    selenium.send_key(input_card_face,'E:\文档\svn文档\自动化\Myproject\QuanminJingjiren\static\img\card_face.png',3)

    input_card_black = selenium.get_xpath( '//ul/li[4]/div/div[2]/div[2]/input',0)
    selenium.send_key(input_card_black,'E:\文档\svn文档\自动化\Myproject\QuanminJingjiren\static\img\card_black.png',3)

    btn_ok = selenium.get_xpath('//button[contains(text(),"确定")]',3)
    selenium.on_click(btn_ok,3)

##### 上传银行卡
    open_userinfo = open_quanminjingjiren+'?r=admin/userinfo'
    selenium.open_url(open_userinfo,1)

    into_mybankcard = selenium.get_xpath('//span[contains(text(),"我的银行卡")]',0)
    selenium.on_click(into_mybankcard,0)

    input_card_holder_name = selenium.get_id('card_holder_name',4)
    selenium.send_key(input_card_holder_name,str(broker_name),0)

    input_select_card = selenium.get_id('bank_id',0)
    selenium.select_options(input_select_card,'4',0)

    input_card_number = selenium.get_id('card_number',0)
    selenium.send_key(input_card_number,'6225000000000001',0)

    input_bank_branch_name = selenium.get_id('bank_branch_name',0)
    selenium.send_key(input_bank_branch_name,'自动化测试_支行名称',0)

    input_bank_city = selenium.get_id('bank_city',0)
    selenium.send_key(input_bank_city,'自动化测试_城市名称',0)

    input_img_card = selenium.get_xpath('//ul/li[7]//input',0)
    selenium.send_key(input_img_card,'E:\文档\svn文档\自动化\Myproject\QuanminJingjiren\static\img\card_blank.png',2)

    btn_card = selenium.get_xpath('//button[contains(text(),"确定")]',0)
    selenium.on_click(btn_card,2)

    selenium.close_browser(3)


def jigoujingjinren(url_jg,broker_compary_phone,broker_name):
    selenium = Selenium.Selenium()
    selenium.loading_Firefox()
    selenium.max_window()
    open_jigoujingjiren  = str(url_jg)+str(Config.IP_Jigoujingjiren)
    selenium.open_url(open_jigoujingjiren,3)
    input_phone = selenium.get_id('phone',0)
    selenium.send_key(input_phone,str(broker_compary_phone),0)
    input_password = selenium.get_id('password',0)
    selenium.send_key(input_password,'123456',0)
    btn_submit = selenium.get_xpath('//a[contains(text(),"登录")]',0)
    selenium.on_click(btn_submit,0)

### 上传身份证
    into_My_IDcard = selenium.get_xpath('//span[contains(text(),"我的身份证")]',2) #进入身份填写页面
    selenium.on_click(into_My_IDcard,0)
    input_name_card = selenium.get_id('name_on_card',0)
    selenium.send_key(input_name_card,str(broker_name),0)
    input_card_number = selenium.get_id('card_number',0)
    selenium.send_key(input_card_number,'152801198703025310',1)

    input_card_face = selenium.get_xpath('//ul/li[3]/div/div[2]/div[2]/input',2)
    selenium.send_key(input_card_face,'E:\文档\svn文档\自动化\Myproject\QuanminJingjiren\static\img\card_face.png',2)

    input_card_black = selenium.get_xpath( '//ul/li[4]/div/div[2]/div[2]/input',0)
    selenium.send_key(input_card_black,'E:\文档\svn文档\自动化\Myproject\QuanminJingjiren\static\img\card_black.png',2)

    btn_ok = selenium.get_xpath('//button[contains(text(),"确定")]',0)
    selenium.on_click(btn_ok,2)

##### 上传银行卡
    open_userinfo = open_jigoujingjiren+'?r=admin/userinfo'
    selenium.open_url(open_userinfo,1)

    into_mybankcard = selenium.get_xpath('//span[contains(text(),"我的银行卡")]',0)
    selenium.on_click(into_mybankcard,0)

    input_card_holder_name = selenium.get_id(str(broker_name),4)
    selenium.send_key(input_card_holder_name,'自动化测试',0)

    input_select_card = selenium.get_id('bank_id',0)
    selenium.select_options(input_select_card,'4',0)

    input_card_number = selenium.get_id('card_number',0)
    selenium.send_key(input_card_number,'6225000000000001',0)

    input_bank_branch_name = selenium.get_id('bank_branch_name',0)
    selenium.send_key(input_bank_branch_name,'自动化测试_支行名称',0)

    input_bank_city = selenium.get_id('bank_city',0)
    selenium.send_key(input_bank_city,'自动化测试_城市名称',0)

    input_img_card = selenium.get_xpath('//ul/li[7]//input',0)
    selenium.send_key(input_img_card,'E:\文档\svn文档\自动化\Myproject\QuanminJingjiren\static\img\card_blank.png',2)

    btn_card = selenium.get_xpath('//button[contains(text(),"确定")]',0)
    selenium.on_click(btn_card,2)

    selenium.close_browser(3)


if __name__ == '__main__':

    # print('运行前置脚本')
    # broker_compary_name = '自动化测试12'
    # broker_compary_phone = '13680001012'
    # admin_cookies = User_login.admin_login_red()
    # broker_compary_id = Broker.creat_Broker_company(admin_cookies,broker_compary_name,broker_compary_phone) # 创建经纪公司
    # broker_companyadmin_name = Broker.savebrokerCompanyAdmin(admin_cookies,broker_compary_id,broker_compary_phone) #创建经纪公司管理员
    # brokerCompany_cookies = User_login.broker_companylogin(broker_companyadmin_name)#经纪公司管理员登陆
    # Broker_company.Broker_mysave(brokerCompany_cookies,broker_compary_phone) #创建经纪人
    # print('经纪公司管理员账号',broker_companyadmin_name)
    # print('经纪人账号:',broker_compary_phone)

    print('')




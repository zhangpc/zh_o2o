# -*- coding:utf-8 -*-
#!/usr/bin/python
import json
import unittest
import unittest
from Fangfull.unittest.TestCase.test_customer import Test_Customer
from flask import Flask,render_template,request,jsonify,redirect,url_for
from config.Config import Flask_Config
from config import Config
from Fangfull.mondel import m_Content_sql,m_Content_url,m_Message_res,m_Message_data
import tools_request
app = Flask(__name__)
sql = Flask_Config
db = sql.get_db()


@app.route('/',methods=['GET'])

def index():
    return render_template('Fangfull/index.html')

@app.route('/Fangfull/add')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result = a + b)

@app.route('/Fangfull/chiocesetting' ,methods=['GET','POST'])
def get_chioce_setting():
    indexid = request.args.get('indexid')
    Content_url = m_Content_url.Content_url
    Content_sql = m_Content_sql.Content_sql
    url_blue = []
    url_red=[]
    sql_id = []
    url_id = []
    sql_name = []
    message_Content_sql = Content_sql.query.all()
    if indexid == None:
        indexid = 1
    message_Content_url = Content_url.query.filter(Content_url.sql_id==indexid).all()
    # print(message_Content_url)
    for message in message_Content_sql:
        sql_id.append(message.sql_id)
        sql_name.append(message.sql_name)

    for message in message_Content_url:
        url_blue.append(message.url_blue)
        url_red.append(message.url_red)
        url_id.append(message.url_id)
    message_url = {'url_blue':url_blue,'url_red':url_red,'sql_id':sql_id,'url_id':url_id,'sql_name':sql_name}

    return jsonify(message_url = message_url,sql_name = sql_name)
    # return render_template('Fangfull/index.html',message_url = message_url,sql_name = sql_name)

# @app.route('/Fangfull/setBasics' ,methods=['GET','POST'])
# def post_setBasics():
#     ipblue = request.args.get('ip_bule')
#     ipred = request.args.get('ip_red')
#     print(ipblue,ipred)
#     return jsonify()





## 获取接口信息
@app.route('/Fangfull/getMessageRes' ,methods=['GET','POST'])
def get_Messageres():
    message_res = m_Message_res.Message_res
    messageres = message_res.query.all()
    res_id = []
    res_name = []
    res_describe = []
    for mes in (messageres):
        res_id.append(mes.res_id)
        res_name.append(mes.res_name)
        res_describe.append(mes.res_describe)
    ms_res = {'res_id':res_id,'res_name':res_name,'res_describe':res_describe}
    return jsonify(MessageRes = ms_res)
    # message_data = m_Message_data.Message_data
    # messagedata = message_data.query.filter(message_data.res_id).all()
    # data_id = []
    # data_name = []
    # data_value = []
    # data_describe = []
    # data_res_id = []
    #
    # for mes in messagedata:
    #     data_id.append(mes.data_id)
    #     data_name.append(mes.data_name)
    #     data_value.append(mes.data_value)
    #     data_describe.append(mes.data_describe)
    #     data_res_id.append(mes.res_id)
    # ms_data = {'data_id':data_id,'data_name':data_name,'data_value':data_value,'data_describe':data_describe,'res_id':data_res_id}
    # print(ms_res)
    # print(ms_data)
    # return jsonify(MessageRes = ms_res,MessageData = ms_data)
#
##获取data值
@app.route('/Fangfull/getMessageData',methods=['GET','POST'])
def get_Messagedata():
    res_id = request.args.get('res_id')
    message_data = m_Message_data.Message_data
    messagedata = message_data.query.filter(message_data.res_id==res_id).all()
    data_id = []
    data_name = []
    data_value = []
    data_describe = []
    data_res_id = []
    for mes in messagedata:
        data_id.append(mes.data_id)
        data_name.append(mes.data_name)
        data_value.append(mes.data_value)
        data_describe.append(mes.data_describe)
        data_res_id.append(mes.res_id)
    ms_data = {'data_id':data_id,'data_name':data_name,'data_value':data_value,'data_describe':data_describe,'res_id':data_res_id}
    print('getMessageData 返回',ms_data)

    # return render_template('/Fangfull/request.html', MessageData=ms_data)
    return jsonify(MessageData=ms_data)

@app.route('/Fangfull/postMessageData',methods=['GET','POST'])
def post_Messagedata():
    data_id = request.args.get('data_id')
    data_name = request.args.get('data_name')
    data_value = request.args.get('data_value')
    data_describe = request.args.get('data_describe')
    message_data = m_Message_data.Message_data
    print(data_id)
    messagedata = message_data.query.filter(message_data.data_id==data_id).first()

    messagedata.data_name = data_name
    messagedata.data_value = data_value
    messagedata.data_describe = data_describe
    sql.submit()
    data = {'data_id':messagedata.data_id,'data_name':messagedata.data_name,'data_value':messagedata.data_value,'data_describe':messagedata.data_describe}

    return jsonify(MessageData=data)
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('Fangfull/page_not_found.html'),404
#
# # @app.route('/Fangfull/setBasics/<basics_mssage>',methods=['GET'])
# @app.route('/Fangfull/setBasics/',methods=['GET','POST'])
# @app.route('/Fangfull/setBasics/<unique_mark>',methods=['GET','POST'])
# def setBasics(basics_mssage=None):
#
#     ipblue = request.args.get('ip_bule')
#     ipred = request.args.get('ip_red')
#     content_sql = request.args.get('content_sql')
#     sqlconnect = Config.SqlConnect()
#     sqlMysql = None
#     if ipblue != '' and ipred!='' and content_sql!='0':
#         if content_sql == '1':
#             sqlMysql = sqlconnect.get_fangfull_test_sql()
#         elif content_sql == '2':
#             sqlMysql = sqlconnect.get_fangfull_beta_sql()
#         basics_mssage = {
#              'ipblue':ipblue,
#              'ipred':ipred,
#              'sqlMysql':sqlMysql,
#              }
#         print(sqlMysql)
#         return jsonify(basics_mssage=basics_mssage)
#         # return render_template('Fangfull/settings.html',basics_mssage = {'a':'1'})
#
#
#
# # @app.route('/Fangfull/getCompanyEmployeeUser',methods=['GET'])
# # def getCompanyEmployeeUser():
# #     return render_template('Fangfull/index.html')
#
# @app.route('/Fangfull/Customeradd',methods=['POST'])
# def postCustomeradd():
#     print('3333')
#     sqlconnect = Config.SqlConnect()
#     sqlMysql = sqlconnect.get_fangfull_test_sql()
#     basics_mssage = {
#          'ipblue':'http://test1www.xqshijie.com/',
#          'ipred':'http://test2www.xqshijie.com/',
#          'sqlMysql':sqlMysql,
#          }
#     zcsacjjy = 'zcsacjjy' ##讲解员职业顾问
#     zcsachtkf = 'zcsachtkf' ## 案场后台客服
#     jg_broker_compary_phone = '13700000118' #机构公司/经纪人登陆账号
#     building_name = '北京中弘大厦' #'新奇世界-半山半岛' '北京中弘大厦'# 新奇世界-长白水镇4号地 #'新奇世界-长白水镇5号地'
#     isdele_customer = True
#     customer_phone = ['13000000162']
#     testcustomer = Test_Customer(basics_mssage,customer_phone,jg_broker_compary_phone,isdele_customer,zcsacjjy,zcsachtkf,building_name)
#     suite = unittest.TestSuite()
#         # # #登录经纪人_添加客户_登录置业顾问添加客户到访_登录客服到访审核通过
#     suite.addTest(testcustomer.test_brokerlogin_addcustomer_customerVisitingRecord_VisitAudited)
#     unittest.TextTestRunner(verbosity=2).run(suite)
#     return render_template('Fangfull/request.html')
#
#
#     # else:
#     #     error = 'Invalid username/password'
#     #     return render_template('Fangfull/index.html', error=error)
#
#     # return render_template('Fangfull/index.html')
#
# # @app.route('/Fangfull/request/',methods=['POST','GET'])
# # @app.route('/Fangfull/request/<name>',methods=['GET'])
# # def request(name = None):
# # #     aa = setBasics()
# # #     print(aa)
# #     # ipblue = request.args.get('ip_bule',0)
# #     # ipred = request.args.get('ip_red',0)
# #     # content_sql = request.args.get('content_sql',0)
# #     # sqlconnect = Config.SqlConnect()
# #     # sqlMysql = None
# #     # if content_sql == '1':
# #     #     sqlMysql = sqlconnect.get_fangfull_test_sql()
# #     # elif content_sql == '2':
# #     #     sqlMysql = sqlconnect.get_fangfull_beta_sql()
# #     # basics_mssage = {
# #     #      'ipblue':ipblue,
# #     #      'ipred':ipred,
# #     #      'sqlMysql':sqlMysql,
# #     #      }
# #     #
# #     # suite = unittest.TestSuite()
# #     # suite.addTest(test_broker_loginaddcustomer_customerVisitingRecord_VisitAudited.test_brokerlogin_addcustomer_customerVisitingRecord_VisitAudited(param=basics_mssage))
# #     # unittest.TextTestRunner(verbosity=2).run(suite)
# #     # return render_template('Fangfull/request.html',locals())
# #
# #     print (basics_message)
# #     return render_template('Fangfull/request.html')
#
#

if __name__ == '__main__':
    app.run(debug=False)

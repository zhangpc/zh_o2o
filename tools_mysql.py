# -*- coding:utf-8 -*-
#!/usr/bin/python
import pymysql

def MysqlConnect(sql,get_sql):

    if sql == None:
        print ('SQL 语句不能是空值')
        return
    try:
        #链接数据库
        conn=pymysql.connect(host=str(get_sql['host']),user=str(get_sql['user']),passwd=str(get_sql['passwd']),port=int(get_sql['port']),charset='utf8')
        cur=conn.cursor()
        conn.select_db(get_sql['db'])

        count=cur.execute(sql)
        results = cur.fetchall()
        Array_result = []

        if len(results) > 0:
            for i in range(len(results)):
                Array_result.append(results[i])
            # print (results[i] ,'   ',results[i][0])


        # print (results)
        # print (count.denominator)
        # print (isinstance(results,list))


        # print (aaa.fetchone())
        # result=cur.fetchall()
        # print (len(result))
        # results = []
        # for i in range(0,len(result)):
        #     results.append(result[i])

        # for r in cur:
        #   print("row_number:" , (cur.rownumber) )
        #   print(str(r[1]))
          # print("id:"+str(r[0])+" name:"+str(r[1])+" password:"+str(r[2]))


        # print ('ID: %s info %s' % result)
        # results=cur.fetchmany(5)
        # for r in results:
        #     print (r)
        #
        # print ('=='*10)
        # cur.scroll(0,mode='absolute')
        # results=cur.fetchall()
        # for r in results:
        #     print (r[1])
        if 'select' not in sql or 'SELECT' not in sql:
            conn.commit()
        cur.close()
        conn.close()

        return Array_result
    except pymysql.Error:
        print ("链接失败" + str(pymysql.Error.args))

if __name__ == "__main__":
    MysqlConnect('select * from customer where customer_id = 2057')

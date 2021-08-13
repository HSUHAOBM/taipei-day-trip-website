from logging import error
import mysql.connector
from datetime import datetime
import configparser
import os
from DBUtils.PooledDB import PooledDB,SharedDBConnection
import pymysql

config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('use_db', 'DBhost')   
DBdatabase=config.get('use_db', 'DBdatabase')
DBuser=config.get('use_db', 'DBuser')
DBpassword=config.get('use_db', 'DBpassword')

def getConnection():
    connection = PooledDB(
    creator=pymysql,
    maxconnections=3,
    mincached=5,
    maxcached=6,maxshared=6,host=DBhost,
    charset='utf8',database=DBdatabase,user=DBuser,password=DBpassword)
    return connection


#旅遊數據數量
def CheakIdCount():
    try:
        connection = getConnection()
        conn = connection.connection()
        cursor = conn.cursor()
        # cursor = connection.cursor()
        cursor.execute("Select count(*) from taipei_trip;")
        records = cursor.fetchone()
        return records[0]
    finally:
        cursor.close()
        conn.close()

#讀取ID的資料
def LoadDataToId(id):
    try:
        connection = getConnection()
        conn = connection.connection()
        cursor = conn.cursor()

        cursor.execute("Select * from taipei_trip where id='%s' limit 1;"%(id))
        records = cursor.fetchone()
        data={
            "id":records[0],
            "name":records[1],
            "category": records[2],
            "description": "，".join(records[3].split("，")[:]),
            "address": records[4],
            "transport": records[5],
            "mrt": records[6],
            "latitude": records[7],
            "longitude": records[8],
            "images": records[9]
        }

        return data

    finally:
        cursor.close()
        conn.close()


#頁數、關鍵字取得資料
def LoadDataToDB(WebPage,WebKeyword):#
    try:
        connection = getConnection()
        conn = connection.connection()
        cursor = conn.cursor()

        if (WebKeyword==None):
            cursor.execute("Select * from taipei_trip limit %d , %d;"%((int(WebPage))*12,12)) 
            records = cursor.fetchall()
            data=[]
            for i in range(len(records)):
                images=[]
                images.append(records[i][9])
                data.append({
                    "id":records[i][0],
                    "name":records[i][1],
                    "category": records[i][2],
                    "description": "，".join(records[i][3].split("，")[:]),
                    "address": records[i][4],
                    "transport": records[i][5],
                    "mrt": records[i][6],
                    "latitude": records[i][7],
                    "longitude": records[i][8],
                    "images": images
                })            
            return data
        if (WebKeyword!=None):
            cursor.execute("SELECT * FROM taipei_trip WHERE stitle Like '%{}%' LIMIT 12 OFFSET {}".format(WebKeyword, int(WebPage)*12))
            records = cursor.fetchall()    
            data=[]
            for i in range(len(records)):
                images=[]
                images.append(records[i][9])
                data.append({
                    "id":records[i][0],
                    "name":records[i][1],
                    "category": records[i][2],
                    "description": "，".join(records[i][3].split("，")[:]),
                    "address": records[i][4],
                    "transport": records[i][5],
                    "mrt": records[i][6],
                    "latitude": records[i][7],
                    "longitude": records[i][8],
                    "images": images
                })
            return data
    finally:
        cursor.close()
        conn.close()

#註冊
def Registered(name,email,password):
    try:
        connection = getConnection()
        conn = connection.connection()
        cursor = conn.cursor()

        #檢查是否註冊過
        cursor.execute("SELECT * FROM membertable WHERE useremail= '%s' limit 1;" % (email))
        records = cursor.fetchone()

            
        if (records):
            # print("註冊過了")
            return {"error": True, "message": "信箱重複註冊!"}

        else:
            # print("開始新增")
            #指令
            sql = "INSERT INTO membertable (username, useremail, userpassword) VALUES (%s, %s, %s);"
            new_data = (name, email, password)
            cursor = conn.cursor()
            cursor.execute(sql, new_data)
            conn.commit()
            return {"ok": True}
    finally:
        cursor.close()
        conn.close()

#登入
def Signin(email,password):
    try:
        connection = getConnection()
        conn = connection.connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id,username,userpassword FROM membertable WHERE useremail= '%s' limit 1;" % (email))
        records = cursor.fetchone()
        if (records):
            # print("帳號正確。。開始檢查密碼")
            # print(records[0],records[1],"的密碼為:"+records[2])

            if (password==records[2]):
                # print("密碼驗證成功")
                return {"ok": True},records
            else:
                # print("密碼錯誤")
                return {"error": True, "message": "帳號或密碼錯誤"},None
        else:
            # print("帳號錯誤")
            return {"error": True, "message": "帳號或密碼錯誤"},None
    finally:
        cursor.close()
        conn.close()

#訂單資料儲存
def Ordersave(useremail,userid,getorderdata,getordersapimessage):
    try:
        connection = getConnection()
        conn = connection.connection()
        cursor = conn.cursor()

        sql = "INSERT INTO ordertable (useremail,userid,tripcost,tripid,tripname,tripaddress,tripimage,tripdate,triptime,contactname,contactemail,contactphone,payment,prime) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        new_data = (useremail, userid, getorderdata["order"]["price"],getorderdata["order"]["trip"]["attraction"]["id"],getorderdata["order"]["trip"]["attraction"]["name"],getorderdata["order"]["trip"]["attraction"]["address"],
        "http://"+getorderdata["order"]["trip"]["attraction"]["images"].split('http://')[1].split(',')[0],getorderdata["order"]["trip"]["date"],getorderdata["order"]["trip"]["time"],getorderdata["order"]["contact"]["name"],getorderdata["order"]["contact"]["email"],getorderdata["order"]["contact"]["phone"],getordersapimessage,getorderdata["prime"])
        cursor = conn.cursor()
        cursor.execute(sql, new_data)
        conn.commit()
        # print("訂單建立成功")
        
        #建立訂單標號
        cursor = conn.cursor()
        cursor.execute("Select id from ordertable where prime='%s';"%(getorderdata["prime"]))
        records = cursor.fetchone()
        tripordernumber=datetime.now().strftime('%Y%m%d')+"triporder"+str(records[0])

        cursor = conn.cursor()
        cursor.execute("UPDATE ordertable set ordernumber='%s' where id = '%d' "%(tripordernumber,records[0]))
        conn.commit()
        # print("訂單回存成功")
        # cursor.execute("UPDATE ordertable SET payment='已付款' where prime='%s';"%(getorderdata["prime"]))
        return tripordernumber
        
    finally:
        cursor.close()
        conn.close()

#更新資料庫            
def Orderupdate(getorderdata):
    try:
        connection = getConnection()
        conn = connection.connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ordertable SET payment='已付款' where prime='%s';"%(getorderdata["prime"]))
        conn.commit()
        # print("訂單付款狀態已更新")
        getordersapimessage="已付款"
        return getordersapimessage
        
    finally:
        cursor.close()
        conn.close()

#取使用者的部分訂單資料
def getordername(useremail):
    getordernameapi={}
    try:
        connection = getConnection()
        conn = connection.connection()
        cursor = conn.cursor()
        cursor.execute("Select ordernumber,tripname,tripdate from ordertable where useremail='%s';"%(useremail))
        records = cursor.fetchall()
        # print("records",records)
        if(records):
            for i in range(len(records)):
                getordernameapi[i+1]={"ordernumber":records[i][0],"tripname":records[i][1],"tripdate":records[i][2]}
        else:
            getordernameapi["error"]=True
        # print(getordernameapi)
        return getordernameapi
    finally:
        cursor.close()
        conn.close()

#取資料庫訂單資料
def getorderdata(ordernumber,useremail):
    try:
        connection = getConnection()
        conn = connection.connection()
        cursor = conn.cursor()
        orderid=ordernumber.split("triporder")[1]
        cursor.execute("Select * from ordertable where id='%s' and useremail='%s';"%(orderid,useremail))
        records = cursor.fetchone()
        if(records):
            orderapi={
              "order": {
                "price": records[3],
                "trip": {
                  "attraction": {
                    "id": records[0],
                    "name": records[5],
                    "address": records[6],
                    "image": records[7]
                  },
                  "date": records[8],
                  "time": records[9]
                },
                "contact": {
                  "name": records[10],
                  "email": records[11],
                  "phone": records[12]
                }
              }
            }
        else: 
            orderapi=None
        return orderapi

    finally:
        cursor.close()
        conn.close()

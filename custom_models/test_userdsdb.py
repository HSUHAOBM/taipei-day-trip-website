import mysql.connector

import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('aws_rd', 'DBhost')   
DBdatabase=config.get('aws_rd', 'DBdatabase')
DBuser=config.get('aws_rd', 'DBuser')
DBpassword=config.get('aws_rd', 'DBpassword')


def uptords(text,imgaesrc):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 


        print("開始新增")
        #指令
        sql = "INSERT INTO message (text, imagesrc) VALUES (%s, %s);"
        new_data = (text, imgaesrc)
        cursor = connection.cursor()
        cursor.execute(sql, new_data)
        connection.commit()
        return {"ok": True}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

def loadtords():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 


        print("開始讀取")
        #指令

        cursor = connection.cursor()
        cursor.execute("select * from message order by time;")
        records = cursor.fetchall()
        myrdsdata=[]
        for i in range(len(records)):
            myrdsdata.append({
                "text":records[i][1],
                "imagesrc":records[i][2]
            })

        # print(myrdsdata)
        return myrdsdata
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
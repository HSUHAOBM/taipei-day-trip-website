import json
import re
import mysql.connector

updata=[]

import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('use_db', 'DBhost')   
DBdatabase=config.get('use_db', 'DBdatabase')
DBuser=config.get('use_db', 'DBuser')
DBpassword=config.get('use_db', 'DBpassword')


with open("data/taipei-attractions.json","r",encoding="utf-8") as json_data:
    data = json.load(json_data)

def getimg(a): #圖片篩選  
    reg="http.*?\.jpg"
    imgre =re.compile(reg)
    imglist_jgp=imgre.findall(a)
#     print("imglist_jpg:",imglist_jgp)
    reg2="http.*?\.png"
    imgre2 =re.compile(reg2)
    imglist_png=imgre2.findall(a)
#     print("imglist2_png:",imglist_png)
    return imglist_jgp+imglist_png

for i in range(len(data["result"]["results"])):
    updata.append([i+1
                   ,data["result"]["results"][i]["stitle"]
                   ,data["result"]["results"][i]["CAT2"]
                   ,data["result"]["results"][i]["xbody"]
                   ,"".join(data["result"]["results"][i]["address"].split(" ")[0::2])
                   ,data["result"]["results"][i]["info"]
                   ,data["result"]["results"][i]["MRT"]
                   ,data["result"]["results"][i]["latitude"]
                   ,data["result"]["results"][i]["longitude"]
                   ,",".join(getimg(",http://".join(data["result"]["results"][i]["file"].lower().split("http://"))))
                  ])


def DataLoadToDB():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = f"""INSERT INTO taipei_trip (id,stitle,category,description,address,transport,mrt,latitude,longitude,images) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

        cursor = connection.cursor()
        cursor.executemany(sql, updata)

        connection.commit()
    finally:
        cursor.close()
        connection.close()
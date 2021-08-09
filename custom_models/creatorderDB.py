import mysql.connector

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

def creatorderDB():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE ordertable  (
            id INT AUTO_INCREMENT PRIMARY KEY,
            useremail VARCHAR(255) NOT NULL,
            userid VARCHAR(255) NOT NULL,
            tripcost INT NOT NULL,
            tripid INT NOT NULL,
            tripname VARCHAR(255) NOT NULL,
            tripaddress VARCHAR(255) NOT NULL,
            tripimage VARCHAR(255) NOT NULL,
            tripdate VARCHAR(255) NOT NULL,
            triptime VARCHAR(255) NOT NULL,
            contactname VARCHAR(255) NOT NULL,
            contactemail VARCHAR(255) NOT NULL,
            contactphone VARCHAR(255) NOT NULL,
            payment VARCHAR(255) NOT NULL,
            prime VARCHAR(255) NOT NULL,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''
            #   ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        
    finally:
        cursor.close()
        connection.close()

#通過 datetime 模組來得到當前時間
# from datetime import datetime
# datetime.now()
# datetime.now().strftime('%Y-%m-%d %H:%M:%S')


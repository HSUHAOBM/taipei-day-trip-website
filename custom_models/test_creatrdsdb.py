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


connection = mysql.connector.connect(
host=DBhost,         
database=DBdatabase, 
user=DBuser,      
password=DBpassword) 

sql = '''CREATE TABLE message  (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(2550) NOT NULL,
    imagesrc VARCHAR(520) NOT NULL,
    time datetime DEFAULT CURRENT_TIMESTAMP);'''
    #   ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

cursor = connection.cursor()
cursor.execute(sql)
connection.commit()

cursor.close()
connection.close()

#通過 datetime 模組來得到當前時間
# from datetime import datetime
# datetime.now()
# datetime.now().strftime('%Y-%m-%d %H:%M:%S')


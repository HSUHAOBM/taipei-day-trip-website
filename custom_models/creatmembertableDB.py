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


connection = mysql.connector.connect(
host=DBhost,         
database=DBdatabase, 
user=DBuser,      
password=DBpassword) 

sql = '''CREATE TABLE  membertable  (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    useremail VARCHAR(255) NOT NULL,
    userpassword VARCHAR(25) NOT NULL,
    time datetime DEFAULT CURRENT_TIMESTAMP);'''
    #   ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

cursor = connection.cursor()
cursor.execute(sql)
connection.commit()

cursor.close()
connection.close()




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



def creattriptableDB():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        sql = '''CREATE TABLE  taipei_trip  (
            id INT AUTO_INCREMENT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            stitle VARCHAR(255),
            category VARCHAR(255)  ,
            description VARCHAR(2550)  ,
            address VARCHAR(128)  ,
            transport VARCHAR(2560)  ,
            mrt VARCHAR(128)  ,
            latitude VARCHAR(255)  ,
            longitude VARCHAR(255)  ,
            images VARCHAR(2550)  );'''
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def creatmembertableDB():
    try:
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
    finally:
        cursor.close()
        connection.close()
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
            ordernumber VARCHAR(50)  ,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''
            #   ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        
    finally:
        cursor.close()
        connection.close()


creattriptableDB()
creatmembertableDB()
creatorderDB()
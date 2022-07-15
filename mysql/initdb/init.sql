create database taipeitrip_web;

CREATE TABLE  taipeitrip_web.taipei_trip  (
            id INT AUTO_INCREMENT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            stitle VARCHAR(255),
            category VARCHAR(255)  ,
            description VARCHAR(2550)  ,
            address VARCHAR(128)  ,
            transport VARCHAR(2560)  ,
            mrt VARCHAR(128)  ,
            latitude VARCHAR(255)  ,
            longitude VARCHAR(255)  ,
            images VARCHAR(2550)  )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  taipeitrip_web.membertable  (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            useremail VARCHAR(255) NOT NULL,
            userpassword VARCHAR(25) NOT NULL,
            time datetime DEFAULT CURRENT_TIMESTAMP)
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
            
CREATE TABLE taipeitrip_web.ordertable  (
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
            time datetime DEFAULT CURRENT_TIMESTAMP)
            ENGINE=InnoDB DEFAULT CHARSET=utf8;

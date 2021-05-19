import mysql.connector
DBhost='localhost'        
DBdatabase='learn_pon'#資料庫
DBuser='root'         #帳號
# DBpassword='HsuanHao_0610'     #密碼
DBpassword='root'     #密碼


#旅遊數據數量
def CheakIdCount():
    connection = mysql.connector.connect(
    host=DBhost,         
    database=DBdatabase, 
    user=DBuser,      
    password=DBpassword) 
    
    cursor = connection.cursor()
    cursor.execute("Select count(*) from taipei_trip;")
    records = cursor.fetchone()
    cursor.close()
    connection.close()
    return records[0]

#讀取ID的資料
def LoadDataToId(id):
    connection = mysql.connector.connect(
    host=DBhost,         
    database=DBdatabase, 
    user=DBuser,      
    password=DBpassword) 
    
    cursor = connection.cursor()
    cursor.execute("Select * from taipei_trip where id='%s';"%(id))
    records = cursor.fetchone()
    images=[]
    images.append(records[9])
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
        "images": images
    }
    cursor.close()
    connection.close()
    return data

#頁數、關鍵字取得資料
def LoadDataToDB(WebPage,WebKeyword):#
    connection = mysql.connector.connect(
    host=DBhost,         
    database=DBdatabase, 
    user=DBuser,      
    password=DBpassword) 
    if (WebKeyword==None):
        cursor = connection.cursor()
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
            cursor.close()
            connection.close()
        return data
    
    if (WebKeyword!=None):
        # print(WebKeyword,WebPage)        
        cursor = connection.cursor()
        # cursor.execute("SELECT * FROM taipei_trip WHERE stitle Like '%{}%' LIMIT {} ,{} ".format(WebKeyword,int(WebPage)*12,12))
        cursor.execute("SELECT * FROM taipei_trip WHERE stitle Like '%{}%' LIMIT 12 OFFSET {}".format(WebKeyword, int(WebPage)*12))
        records = cursor.fetchall()    
        # print(len(records))
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
            cursor.close()
            connection.close()
        return data

#註冊
def Registered(name,email,password):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        #檢查是否註冊過
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM membertable WHERE useremail= '%s';" % (email))
        records = cursor.fetchone()

            
        if (records):
            print("註冊過了")
            return {"error": True, "message": "信箱重複註冊!"}

        else:
            print("開始新增")
            #指令
            sql = "INSERT INTO membertable (username, useremail, userpassword) VALUES (%s, %s, %s);"
            new_data = (name, email, password)
            cursor = connection.cursor()
            cursor.execute(sql, new_data)
            connection.commit()
            return {"ok": True}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")


def Signin(email,password):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      # 資料庫帳號
        password=DBpassword)  # 資料庫密碼

        #檢查是否註冊過
        cursor = connection.cursor()
        cursor.execute("SELECT id,username,userpassword FROM membertable WHERE useremail= '%s';" % (email))
        records = cursor.fetchone()
        if (records):
            print("帳號正確。。開始檢查密碼")
            # print(records[0],records[1],"的密碼為:"+records[2])

            if (password==records[2]):
                print("密碼驗證成功")
                return {"ok": True},records
            else:
                print("密碼錯誤")
                return {"error": True, "message": "帳號或密碼錯誤"},None
        else:
            print("帳號錯誤")
            return {"error": True, "message": "帳號或密碼錯誤"},None
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

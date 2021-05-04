import mysql.connector
DBhost='localhost'        
DBdatabase='learn_pon'#資料庫
DBuser='root'         #帳號
DBpassword='HsuanHao_0610'     #密碼
# DBpassword='root'     #密碼

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
#     if(records)
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
        # cursor.execute("Select * from taipei_trip ")

        
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
        print(WebKeyword)        
        cursor = connection.cursor()
        # cursor.execute("Select * from taipei_trip where stitle like %s;" , ("%" + WebKeyword + "%",))
        params=['%'+WebKeyword+'%']
        sql_select="Select * from taipei_trip where stitle like %s;"
        cursor.execute(sql_select,params)

        # cursor.execute("Select * from taipei_trip where stitle like '%台北%'")




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
from flask import *
from requests.api import get
from custom_models import UseData, apianalysis,usetappay

from flask_cors import CORS

getdata = {}

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/")
CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'laowangaigebi'  # key


# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    request.args.get("number",None) #使用max無資料則使用None
    useremail = session.get('useremail')    
    if useremail:
        return render_template("thankyou.html")
    else:
        return redirect("/")  


@app.route("/attraction/<id>")
def attraction(id):
    IdCount = UseData.CheakIdCount()
    attractionId = int(id)
    if attractionId <= int(IdCount) and attractionId >= 1:
        return render_template("attraction.html")
    else:
        abort(400)


@app.route("/api/booking", methods=["POST", "GET", "PATCH", "DELETE"])
def apibooking():
    useremail = session.get('useremail')
    username = session.get('username')
    userid = session.get('id')
    if useremail and username and userid:
        if request.method == "GET":
            return Response(json.dumps(getdata, sort_keys=False), mimetype='application/json')

        if request.method == "POST":
            orderdata = request.get_json()
            id = orderdata['attractionId']
            apigetdata = apianalysis.apiget(id)
            getdata["data"] = {}
            getdata["data"]["attraction"] = apigetdata
            getdata["data"]["date"] = orderdata['date']
            getdata["data"]["time"] = orderdata['time']
            getdata["data"]["price"] = orderdata['price']
            if getdata != None:
                return {"ok": True}
            if getdata == None:
                return abort(400)
            else:
                return abort(500)

        if request.method == "DELETE":
            getdata.clear()
            return {"ok": True}
    else:
        return{"error": True, "message": "未登入"}, 403
        # return render_template("booking.html")


# http://127.0.0.1:3000/api/attractions?page=?&keyword=?
@app.route("/api/attractions")
def getbaseapi():
    WebPage = request.args.get("page", 0)
    WebKeyword = request.args.get("keyword", None)
    data = UseData.LoadDataToDB(WebPage, WebKeyword)
    # data=data[12*int(WebPage):12*(int(WebPage)+1)]
    if (len(data) >= 12):
        return Response(json.dumps({"nextpage": int(WebPage)+1, "data": data}, sort_keys=False), mimetype='application/json')
    if (len(data) < 12) and (len(data) >= 1):
        return Response(json.dumps({"nextpage": None, "data": data}, sort_keys=False), mimetype='application/json')
    else:
        abort(500)


@app.errorhandler(400)
def page_400(error):
    return Response(json.dumps({"error": True, "message": "建立錯誤"}, sort_keys=False), mimetype='application/json'), 400


@app.errorhandler(500)
def page_500(error):
    return Response(json.dumps({"error": True, "message": "伺服器內部錯誤"}, sort_keys=False), mimetype='application/json'), 500


@app.route("/api/attraction/<attractionId>")
def attractionId(attractionId):
    IdCount = UseData.CheakIdCount()
    attractionId = int(attractionId)
    if attractionId <= int(IdCount) and attractionId >= 1:
        data = UseData.LoadDataToId(attractionId)
        return Response(json.dumps({"data": data}, sort_keys=False), mimetype='application/json')
    else:
        abort(400)


@app.route("/api/user", methods=["POST", "GET", "PATCH", "DELETE"])
def usercheck():
    # print("request.method:", request.method) 連線方式
    useremail = session.get('useremail')
    username = session.get('username')
    userid = session.get('id')
    if useremail and username and userid:
        # 檢核登入狀態
        if request.method == "GET":
            print("登入中")
            return {"data": {
                "id": userid,
                "name": username,
                "email": useremail}}
        # 登出
        if request.method == "DELETE":
            session.clear()            
            getdata.clear()
            return {"ok": True}
    else:
        data = request.get_json()
        if data != None:
            useremail = data['email']
            userpassword = data['password']
            # 註冊
            if(data.get('name') != None and request.method == "POST"):
                username = data['name']
                # 檢查輸入是否為空白
                if not useremail.strip() or not userpassword.strip() or not username.strip():
                    return {"error": True, "message": "檢查輸入是否為空白!"}
                else:
                    state = UseData.Registered(
                        username, useremail, userpassword)
                    data = {}
                    return state
            # 登入
            if(data.get('name') == None and request.method == "PATCH"):
                # 檢查輸入是否為空白
                if not useremail.strip() or not userpassword.strip():
                    return {"error": True, "message": "檢查輸入是否為空白!"}
                else:
                    state, DBloaddata = UseData.Signin(useremail, userpassword)
                    if(state.get('ok')):
                        session['useremail'] = useremail
                        session['username'] = DBloaddata[1]
                        session['id'] = DBloaddata[0]
                        print("session", session)
                    data = {}
                    return state
        else:
            return {"data": None}


@app.route("/api/orders", methods=["POST", "GET"])
def getordersapi():
    useremail = session.get('useremail')    
    userid = session.get('id')
    getordersapimessage="未付款"

    if useremail :            
        getorderdata = request.get_json()
        #訂單存進資料庫
        tripordernumber=UseData.Ordersave(useremail,userid,getorderdata,getordersapimessage)
        #連線取訂單付款
        tappaypaybyprime=usetappay.paybyprime(getorderdata)
        if tappaypaybyprime["status"]==0:
            getordersapimessage=UseData.Orderupdate(getorderdata)
            getordersapi={"data":
                {"number": tripordernumber,
                "payment": {
                    "status": 0,
                    "message": getordersapimessage
                    }
                }
            }
        else:
            return {"error": True, "message": tripordernumber+"訂單錯誤"}, 400
        return getordersapi

    else:
        return{"error": True, "message": "未登入"}, 403

@app.route("/api/orders/<ordernumber>")
def getordataapi(ordernumber):

    useremail = session.get('useremail')    
    if useremail :            
        orderdataapi=UseData.getorderdata(ordernumber,useremail)
        return Response(json.dumps(orderdataapi, sort_keys=False), mimetype='application/json')

    else:
        return{"error": True, "message": "未登入"}, 403        




# @app.route("/123")
# def index123():
#     return render_template("test2.html")


# @app.route("/321")
# def index321():
#     return render_template("example.html")


# app.run(host="0.0.0.0", port=3000)
app.run(port=3000, debug=True)
# app.run(port=3000)

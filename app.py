from flask import *
from custom_models import UseData

from flask_cors import CORS

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


@app.route("/attraction/<id>")
def attraction(id):
    IdCount = UseData.CheakIdCount()
    attractionId = int(id)
    if attractionId <= int(IdCount) and attractionId >= 1:
        return render_template("attraction.html")
    else:
        abort(400)


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


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
    return Response(json.dumps({"error": True, "message": "自訂的錯誤訊息"}, sort_keys=False), mimetype='application/json'), 400


@app.errorhandler(500)
def page_500(error):
    return Response(json.dumps({"error": True, "message": "自訂的錯誤訊息"}, sort_keys=False), mimetype='application/json'), 500


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
            return {"ok": True}
    else:
        data = request.get_json()
        if data != None:
            useremail = data['email']
            userpassword = data['password']
            # 註冊
            if(data.get('name') != None and request.method == "POST"):
                username = data['name']
                #檢查輸入是否為空白
                if not useremail.strip() or not userpassword.strip() or not username.strip():
                    return {"data": None}
                else:    
                    state = UseData.Registered(username, useremail, userpassword)
                    data = {}
                    return state
            # 登入
            if(data.get('name') == None and request.method == "PATCH"):
                #檢查輸入是否為空白
                if not useremail.strip() or not userpassword.strip():
                    return {"data": None}
                else:
                    state, DBloaddata = UseData.Signin(useremail, userpassword)
                    if(state.get('ok')):
                        session['useremail'] = useremail
                        session['username'] = DBloaddata[1]
                        session['id'] = DBloaddata[0]
                        print("session",session)
                    data = {}
                    return state
        else:
            return {"data": None}




app.run(host="0.0.0.0", port=3000)
# app.run(port=3000, debug=True)
# app.run(port=3000)

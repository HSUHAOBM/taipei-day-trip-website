from flask import *
import mysql.connector
from custom_models import UseData

from flask_cors import CORS


app=Flask(
    __name__,
    static_folder="static",
    static_url_path="/")
CORS(app)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True




# Pages
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")
@app.route("/booking")
def booking():
    return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/api/attractions")   #http://127.0.0.1:3000/api/attractions?page=?&keyword=?
def getbaseapi():
    WebPage=request.args.get("page",0) 
    WebKeyword=request.args.get("keyword",None)   
    print("WebPage:",WebPage,"WebKeyword:",WebKeyword)
    data=UseData.LoadDataToDB(WebPage,WebKeyword)

    data=data[12*int(WebPage):12*(int(WebPage)+1)]
    if (len(data)>=12):
        if (len(data)==12):
            return Response(json.dumps({"nextpage":int(WebPage)+1,"data":data}, sort_keys=False),mimetype='application/json')
    if (len(data)<12) and (len(data)>=1):
        return Response(json.dumps({"nextpage":None,"data":data}, sort_keys=False),mimetype='application/json')
    else:
        abort(500)


@app.errorhandler(400)
def page_400(error):
    return Response(json.dumps({"error":True,"message": "自訂的錯誤訊息"}, sort_keys=False),mimetype='application/json'),400

@app.errorhandler(500)
def page_500(error):
    return Response(json.dumps({"error":True,"message": "自訂的錯誤訊息"}, sort_keys=False),mimetype='application/json'),500

@app.route("/api/attraction/<attractionId>")
def attractionId(attractionId):
    IdCount=UseData.CheakIdCount()
    attractionId=int(attractionId)
    if attractionId<=int(IdCount) and attractionId>=1:
        data=UseData.LoadDataToId(attractionId)
        return Response(json.dumps({"data":data}, sort_keys=False),mimetype='application/json')
    else:
        abort(400)



app.run(host="0.0.0.0", port=3000)
# app.run(port=3000)


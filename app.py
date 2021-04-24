from flask import *
import mysql.connector
from custom_models import UseData


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True




# Pages
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
    IdCount=UseData.CheakIdCount()
    id=int(id)
    if id<=int(IdCount) and id>=1:
        data=UseData.LoadDataToId(id)
        return Response(json.dumps({"data":data}, sort_keys=False),mimetype='application/json')
    else:
        abort(400)
    #     return render_template("attraction.html")
@app.route("/booking")
def booking():
    return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/api/attraction")   #http://127.0.0.1:3000/api/attraction?page=?&keyword=?
def getbaseapi():
    WebPage=request.args.get("page",1) 
    WebKeyword=request.args.get("keyword",None)   
    print("WebPage:",WebPage,"WebKeyword:",WebKeyword)
    data=UseData.LoadDataToDB(WebPage,WebKeyword)
#   return jsonify({"nextpage":WebPage,"data":data})
    if (len(data)>=1):
        return Response(json.dumps({"nextpage":WebPage,"data":data}, sort_keys=False),mimetype='application/json')
    else:
        abort(500)


@app.errorhandler(400)
def page_400(error):
    return Response(json.dumps({"error":True,"message": "自訂的錯誤訊息"}, sort_keys=False),mimetype='application/json'),400

@app.errorhandler(500)
def page_500(error):
    return Response(json.dumps({"error":True,"message": "自訂的錯誤訊息"}, sort_keys=False),mimetype='application/json'),500



app.run(port=3000)


